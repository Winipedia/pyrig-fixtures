"""Catch-all module for shared pytest fixtures with no more specific home.

Fixtures scaffolded without a dedicated topic are appended here rather than
sorted into one of the other themed fixture modules.
"""

import os
import re
import shutil
from contextlib import chdir, suppress
from pathlib import Path

import pyrig
import pytest
from pyrig.rig.cli.subcommands import init
from pyrig.rig.configs.base.config_file import ConfigFile
from pyrig.rig.configs.pyproject import PyprojectConfigFile
from pyrig.rig.tools.packages.manager import PackageManager
from pyrig.rig.tools.pyrigger import Pyrigger
from pyrig.rig.tools.testing.project import ProjectTester
from pyrig.rig.tools.version_control.controller import VersionController
from pyrig_runtime.core.dependencies.discovery import dependency_ancestors
from pyrig_runtime.core.strings import kebab_to_snake_case, snake_to_kebab_case
from pyrig_runtime.rig.cli.shared_subcommands import version


@pytest.fixture(scope="session", autouse=True)
def init_pyrig_project(
    tmp_path_factory: pytest.TempPathFactory,
) -> tuple[bool, str]:
    """Initialize a pyrig project and return a tuple indicating success or error."""
    tmp_path = tmp_path_factory.mktemp(init_pyrig_project.__name__)
    with pytest.MonkeyPatch.context() as monkeypatch:
        return run_init_pyrig_project(tmp_path, monkeypatch)


def run_init_pyrig_project(  # noqa: PLR0915
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> tuple[bool, str]:
    """Run the steps behind `init_pyrig_project` and report success or failure.

    Extracted into a plain function, rather than inlined in the fixture, so
    tests can call it directly with mocked subprocess results to exercise
    each of its failure branches.
    """
    # on Actions windows-latest temp path is on another drive so add path fails
    # so we use a tmp dir in the current dir
    # now test that in an empty folder with a pyproject.toml file
    # with a folder src that the setup works

    # copy the pyrig package to tmp_path/pyrig with shutil
    project_name = "src-project"

    pyrig_tmp_path = tmp_path / PackageManager.I.project_name()
    shutil.copytree(
        Path(),
        pyrig_tmp_path,
    )
    with chdir(pyrig_tmp_path):
        # remove a potential dist dir from a previous build
        dist_dir = pyrig_tmp_path / "dist"
        with suppress(FileNotFoundError):
            shutil.rmtree(dist_dir)
        # build the package
        args = PackageManager.I.build_args()
        args.run()

    dist_files = list((pyrig_tmp_path / "dist").glob("*.whl"))
    wheel_path = dist_files[-1].resolve().as_posix()

    src_project_dir = tmp_path / project_name
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
            snake_to_kebab_case(dep.__name__) for dep in dependency_ancestors(pyrig)
        )

        # add plugins
        PackageManager.I.add_dev_dependencies_args(wheel_path, *plugins).run()

        # uv add converts absolute paths to relative paths, which breaks when
        # the project is copied to a different location (e.g., in the
        # no_dev_deps_in_source_code fixture). We need to replace the
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
        args = PackageManager.I.run_args(project_name, "--help")
        res = args.run()
        stdout = res.stdout
        expected = project_name
        if expected not in stdout.lower():
            return (
                False,
                "Expected the projects CLI to work and find the project name in stdout",
            )

        # assert calling version works
        args = PackageManager.I.run_args(project_name, version.__name__)
        res = args.run()
        stdout = res.stdout
        expected = f"{project_name} 0.1.0"
        if expected not in stdout:
            return (
                False,
                f"Expected the projects version command to output '{expected}'",
            )

        package_dir = src_project_dir / "src" / kebab_to_snake_case(project_name)
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
