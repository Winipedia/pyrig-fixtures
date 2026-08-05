"""Catch-all module for shared pytest fixtures with no more specific home.

Fixtures scaffolded without a dedicated topic are appended here rather than
sorted into one of the other themed fixture modules.
"""

import os
import re
import shutil
from contextlib import chdir, suppress
from pathlib import Path
from tempfile import TemporaryDirectory

import pyrig_runtime
import pytest
from pyrig.rig.cli.subcommands import init
from pyrig.rig.configs.base.config_file import ConfigFile
from pyrig.rig.configs.pyproject import PyprojectConfigFile
from pyrig.rig.tools.packages.manager import PackageManager
from pyrig.rig.tools.pyrigger import Pyrigger
from pyrig.rig.tools.testing.project import ProjectTester
from pyrig.rig.tools.version_control.controller import VersionController
from pyrig_runtime.core.dependencies.discovery import dependent_packages
from pyrig_runtime.core.strings import kebab_to_snake_case, snake_to_kebab_case
from pyrig_runtime.rig.cli.shared_subcommands import version

SKIP_INIT_PYRIG_PROJECT_FLAG_NAME = "skip-init-pyrig-project"

SKIP_INIT_PYRIG_PROJECT_FLAG = f"--{SKIP_INIT_PYRIG_PROJECT_FLAG_NAME}"
SKIP_INIT_PYRIG_PROJECT_SHORT_FLAG = (
    f"--{''.join(part[0] for part in SKIP_INIT_PYRIG_PROJECT_FLAG_NAME.split('-'))}"
)


def pytest_addoption(parser: pytest.Parser) -> None:
    """Register the `--skip-init-pyrig-project` command-line flag.

    The flag lets a run opt out of the expensive [init_pyrig_project][]
    fixture that every project depending on pyrig-fixtures otherwise runs
    once per test session, e.g. for a fast local feedback loop.

    A true single-dash short form (e.g. `-sipp`) isn't possible: pytest
    reserves lowercase single-dash options for its own core and rejects
    them from plugins, so `--sipp` is offered as the short alias instead.

    Args:
        parser: Pytest's parser to register the command-line option on.
    """
    parser.addoption(
        SKIP_INIT_PYRIG_PROJECT_FLAG,
        SKIP_INIT_PYRIG_PROJECT_SHORT_FLAG,
        action="store_true",
        default=False,
        help="Skip the slow `init_pyrig_project` end-to-end fixture.",
    )


def claim_file(tmp_path_factory: pytest.TempPathFactory, stem: str) -> bool:
    """Try to exclusively claim a `<stem>.claimed` marker file.

    Every pytest-xdist worker's own base temp dir is `<root>/<worker_id>`,
    so `<root>` is the same shared path in every worker regardless of how
    many exist or how tests get distributed among them. Creating the marker
    there via `Path.touch(exist_ok=False)` is atomic on every platform
    pytest supports, so exactly one caller across all workers ever wins the
    race.

    Args:
        tmp_path_factory: Used to locate the shared `<root>` dir.
        stem: Distinguishes this claim from any other's marker file.

    Returns:
        `True` for the one caller that wins the race, `False` for every
        other caller.
    """
    marker = tmp_path_factory.getbasetemp().parent / f"{stem}.claimed"
    try:
        marker.touch(exist_ok=False)
    except FileExistsError:
        return False
    return True


@pytest.fixture(scope="session", autouse=True)
def init_pyrig_project(
    request: pytest.FixtureRequest,
    tmp_path_factory: pytest.TempPathFactory,
) -> tuple[bool, str]:
    """Verify that this project can be built and adopted by a fresh consumer project.

    Delegates the actual build, install, and verification flow to
    [run_init_pyrig_project][], once per test session, in an isolated
    temporary directory. Skipped when `--skip-init-pyrig-project` is
    passed.

    Under pytest-xdist, every worker process would otherwise repeat this
    expensive flow independently. [claim_file][] elects a single winner,
    across however many worker processes exist, to run it for real; outside
    of pytest-xdist there's only one process, so it always wins trivially.

    Args:
        request: Used to read the `--skip-init-pyrig-project` option.
        tmp_path_factory: Used to locate the shared dir to race for the
            claim in.

    Returns:
        A tuple of `(success, message)`, where `success` is always `True`
        since a failed check raises instead of returning. `message`
        explains why the run was skipped, or is empty when it ran and
        succeeded.

    Raises:
        pytest.fail.Exception: If the check does not succeed.

    Note:
        Being autouse and session-scoped, a failed check reports a setup
        error for every test in the session, not just one. Under
        pytest-xdist, that only holds for the winning worker's own tests,
        since it's the only one that actually runs the check — the other
        workers' tests are unaffected either way, but the run as a whole
        still fails since the winner's tests do.
    """
    if request.config.getoption(SKIP_INIT_PYRIG_PROJECT_FLAG):
        return True, f"Skipped via {SKIP_INIT_PYRIG_PROJECT_FLAG}"

    if not claim_file(tmp_path_factory, init_pyrig_project.__name__):
        return True, "Skipped: another worker already claimed this check"

    with (
        TemporaryDirectory() as tmp_dir,
        pytest.MonkeyPatch.context() as monkeypatch,
    ):
        success, msg = run_init_pyrig_project(Path(tmp_dir), monkeypatch)

    if not success:
        pytest.fail(f"Failed to initialize pyrig project: {msg}")
    return success, msg


def run_init_pyrig_project(  # noqa: PLR0915
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> tuple[bool, str]:
    """Build this project and verify a fresh consumer project can adopt it.

    Packages the current project as a wheel and scaffolds a brand-new
    project under `tmp_path`, adding the wheel plus every other
    currently-installed plugin that depends on pyrig-runtime as dev
    dependencies. Runs `pyrig init` in the new project, then checks that
    its own test suite fails as expected, that its CLI and `version`
    command produce the expected output, that the expected package
    directory was generated, and that every `ConfigFile` subclass
    produced its file. Finally runs `pyrigger --help` as a last sanity
    check.

    Kept as a standalone function, separate from [init_pyrig_project][],
    so tests can call it directly with mocked subprocess results to
    exercise each failure branch independently.

    Args:
        tmp_path: Scratch directory to scaffold the wheel-build copy of
            this project and the new consumer project under; must not
            already contain directories with their names.
        monkeypatch: Used to remove the current virtual environment from
            the environment for the duration of the run, so subprocess
            commands create and use their own fresh environment instead
            of reusing the caller's.

    Returns:
        A tuple of `(success, message)`. `success` is `True` only if
        every check above passes; `message` describes the first check
        that failed, or is empty when `success` is `True`.

    Raises:
        subprocess.CalledProcessError: If any underlying command fails,
            other than the new project's own test suite exiting as
            expected.
    """
    src_project_name = "src-project"

    pyrig_project_tmp_path = tmp_path / PackageManager.I.project_name()
    shutil.copytree(
        Path(),
        pyrig_project_tmp_path,
    )
    with chdir(pyrig_project_tmp_path):
        # remove a potential dist dir from a previous build
        dist_dir = pyrig_project_tmp_path / "dist"
        with suppress(FileNotFoundError):
            shutil.rmtree(dist_dir)
        # build the package
        args = PackageManager.I.build_args()
        args.run()

    dist_files = list((pyrig_project_tmp_path / "dist").glob("*.whl"))
    wheel_path = dist_files[-1].resolve().as_posix()

    src_project_dir = tmp_path / src_project_name
    src_project_dir.mkdir()

    # Get the current Python version in major.minor format
    python_version = str(PyprojectConfigFile.I.first_supported_python_version())

    with chdir(src_project_dir):
        # Strip VIRTUAL_ENV and the outer venv's bin dir from PATH so
        # subprocesses create a new virtual environment instead of reusing
        # the current one, and commands like `pyrig` from the dev environment
        # aren't found when testing that they're absent.
        venv = os.environ.get("VIRTUAL_ENV")
        monkeypatch.delenv("VIRTUAL_ENV", raising=False)
        if venv:
            path_entries = os.environ.get("PATH", "").split(os.pathsep)
            monkeypatch.setenv(
                "PATH",
                os.pathsep.join(
                    p for p in path_entries if not p.lower().startswith(venv.lower())
                ),
            )

        # Initialize git repo in the test project directory
        VersionController.I.init_args().run()
        VersionController.I.config_args(
            "--local",
            "user.email",
            "test@example.com",
        ).run()
        VersionController.I.config_args("--local", "user.name", "Test User").run()

        args = PackageManager.I.args("init", "--python", python_version)
        args.run()

        # Add pyrig wheel as a dev dependency and plugins
        plugins = tuple(
            snake_to_kebab_case(dep.__name__)
            for dep in dependent_packages(pyrig_runtime)
            # wheel path is the package name, so don't add it as a dependency twice
            if dep.__name__ != PackageManager.I.package_name()
        )

        # add plugins
        PackageManager.I.add_group_dev_args(wheel_path, *plugins).run()

        # uv add converts absolute paths to relative paths, which breaks when
        # the project is copied to a different location. We need to replace the
        # relative path with an absolute path.
        pyproject_toml = src_project_dir / "pyproject.toml"
        pyproject_content = pyproject_toml.read_text(encoding="utf-8")
        # Replace relative path with absolute path in tool.uv.sources
        # e.g., { path = "../pyrig/dist/..." }
        # -> { path = "/tmp/.../pyrig/dist/..." }
        pyproject_content = re.sub(
            r'pyrig = \{ path = "[^"]*" \}',
            f'pyrig = {{ path = "{wheel_path}" }}',
            pyproject_content,
        )
        pyproject_toml.write_text(pyproject_content, encoding="utf-8")

        # Sync to update the lock file with the new absolute path
        args = PackageManager.I.install_dependencies_args()
        args.run()

        # Verify pyrig was installed correctly
        # also checks if the init process works
        PackageManager.I.run_args(*Pyrigger.I.cmd_args(cmd=init)).run()

        # with cov
        args = PackageManager.I.run_args(*ProjectTester.I.test_args())
        res = args.run(check=False)
        if res.returncode != pytest.ExitCode.TESTS_FAILED:
            return False, f"Expected tests to fail, got return code {res.returncode}"

        # assert the packages own cli is available
        args = PackageManager.I.run_args(src_project_name, "--help")
        res = args.run()
        stdout = res.stdout
        expected = src_project_name
        if expected not in stdout.lower():
            return (
                False,
                "Expected the projects CLI to work and find the project name in stdout",
            )

        # assert calling version works
        args = PackageManager.I.run_args(src_project_name, version.__name__)
        res = args.run()
        stdout = res.stdout
        expected = f"{src_project_name} 0.1.0"
        if expected not in stdout:
            return (
                False,
                f"Expected the projects version command to output '{expected}'",
            )

        package_dir = src_project_dir / "src" / kebab_to_snake_case(src_project_name)
        if not package_dir.exists():
            return (
                False,
                f"Expected package directory {package_dir} to exist after init",
            )

        for cf in ConfigFile.concrete_subclasses():
            if not cf().path().exists():
                return (
                    False,
                    f"Expected config file {cf().path()} to exist after init",
                )

        PackageManager.I.run_args(*Pyrigger.I.args("--help")).run()

    return True, ""
