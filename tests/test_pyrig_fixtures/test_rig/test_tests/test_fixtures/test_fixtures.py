"""Test module."""

import shutil
import subprocess
from collections.abc import Callable, Iterator
from pathlib import Path

import pytest
from pyrig.core.subprocesses import Args
from pyrig_runtime.core.strings import kebab_to_snake_case
from pyrig_runtime.rig.cli.shared_subcommands import version
from pytest_mock import MockerFixture

from pyrig_fixtures.rig.tests.fixtures.fixtures import run_init_pyrig_project


def test_init_pyrig_project(init_pyrig_project: tuple[bool, str]) -> None:
    """Test function."""
    success, message = init_pyrig_project
    assert success, message


def test_run_init_pyrig_project() -> None:
    """Test function."""
    assert callable(run_init_pyrig_project)


def test_init_pyrig_project_fails(  # noqa: C901, PLR0915
    mocker: MockerFixture,
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    """Test function.

    `run_init_pyrig_project` is a real, slow, end-to-end flow (git, uv,
    pytest, ...). To exercise its failure branches without paying for any of
    that, its subprocess calls and initial project copy are faked here, so
    this test stays fast and hermetic.
    """
    project_name = "src-project"

    # `test_init_pyrig_project` covers the branch where `VIRTUAL_ENV` is set;
    # unset it here so these scenarios cover the other branch.
    monkeypatch.delenv("VIRTUAL_ENV", raising=False)

    def fake_copytree(_src: Path, dst: Path) -> None:
        """Scaffold a directory instead of really copying the project.

        Also leaves a stale `dist/` dir behind, as if from a previous build,
        to exercise its cleanup branch.
        """
        dst.mkdir(parents=True, exist_ok=True)
        (dst / "dist").mkdir(exist_ok=True)

    mocker.patch.object(shutil, "copytree", fake_copytree)

    real_glob = Path.glob

    def fake_glob(self: Path, pattern: str) -> Iterator[Path]:
        """Make wheel discovery find a fake wheel without a real build."""
        if pattern == "*.whl":
            return iter([Path("fake-0.1.0-py3-none-any.whl")])
        return real_glob(self, pattern)

    mocker.patch.object(Path, "glob", fake_glob)

    def default_result(
        args: Args,
        *,
        check: bool,
    ) -> subprocess.CompletedProcess[str]:
        """Fabricate the "everything is fine" result for one `Args.run()` call."""
        if check is False and "--no-cov" in args:
            return subprocess.CompletedProcess(args, pytest.ExitCode.NO_TESTS_COLLECTED)
        if check is False:
            return subprocess.CompletedProcess(args, pytest.ExitCode.TESTS_FAILED)
        if "init" in args and "--python" in args:
            # `uv init` would normally scaffold `pyproject.toml`; fake that too.
            Path("pyproject.toml").write_text(
                '[tool.uv.sources]\npyrig = { path = "../fake.whl" }\n',
                encoding="utf-8",
            )
        if project_name in args and "--help" in args:
            return subprocess.CompletedProcess(args, 0, stdout=project_name)
        if project_name in args and version.__name__ in args:
            return subprocess.CompletedProcess(args, 0, stdout=f"{project_name} 0.1.0")
        return subprocess.CompletedProcess(args, 0, stdout="")

    def mock_run(
        override: Callable[[Args, bool, subprocess.CompletedProcess[str]], None]
        | None = None,
    ) -> None:
        """Replace `Args.run` with a fully fake, instant implementation."""

        def fake_run(
            self: Args,
            *,
            check: bool = True,
        ) -> subprocess.CompletedProcess[str]:
            """Fabricate a result, then let `override` tweak it if given."""
            result = default_result(self, check=check)
            if override is not None:
                override(self, check, result)
            return result

        mocker.patch.object(Args, "run", fake_run)

    def run_scenario(name: str) -> tuple[bool, str]:
        """Run `run_init_pyrig_project` in a fresh, fully mocked directory."""
        scenario_path = tmp_path / name
        scenario_path.mkdir()
        with pytest.MonkeyPatch.context() as scenario_monkeypatch:
            return run_init_pyrig_project(scenario_path, scenario_monkeypatch)

    def force_no_tests_collected_mismatch(
        args: Args,
        check: bool,  # noqa: FBT001
        result: subprocess.CompletedProcess[str],
    ) -> None:
        """Make the `--no-cov` pytest run return an unexpected exit code."""
        if check is False and "--no-cov" in args:
            result.returncode = 0

    mock_run(force_no_tests_collected_mismatch)
    success, message = run_scenario("no_tests_collected")
    assert success is False
    assert "Expected no tests collected" in message

    def force_tests_failed_mismatch(
        args: Args,
        check: bool,  # noqa: FBT001
        result: subprocess.CompletedProcess[str],
    ) -> None:
        """Make the coverage pytest run return an unexpected exit code."""
        if check is False and "--no-cov" not in args:
            result.returncode = 0

    mock_run(force_tests_failed_mismatch)
    success, message = run_scenario("tests_failed")
    assert success is False
    assert "Expected tests to fail" in message

    def force_cli_help_mismatch(
        args: Args,
        check: bool,  # noqa: FBT001
        result: subprocess.CompletedProcess[str],
    ) -> None:
        """Make the CLI `--help` run print unexpected output."""
        if check is True and project_name in args and "--help" in args:
            result.stdout = ""

    mock_run(force_cli_help_mismatch)
    success, message = run_scenario("cli_help")
    assert success is False
    assert "Expected the projects CLI to work" in message

    def force_cli_version_mismatch(
        args: Args,
        check: bool,  # noqa: FBT001
        result: subprocess.CompletedProcess[str],
    ) -> None:
        """Make the CLI `version` run print unexpected output."""
        if check is True and project_name in args and version.__name__ in args:
            result.stdout = ""

    mock_run(force_cli_version_mismatch)
    success, message = run_scenario("cli_version")
    assert success is False
    assert "Expected the projects version command" in message

    # The remaining checks are filesystem-based; a plain fake run reaches
    # them, and the package directory / config files naturally don't exist
    # since no real `pyrig init` ever ran.
    mock_run()
    success, message = run_scenario("package_missing")
    assert success is False
    assert "Expected package directory" in message

    real_exists = Path.exists
    expected_package_dir = (
        tmp_path
        / "config_missing"
        / project_name
        / "src"
        / kebab_to_snake_case(project_name)
    )

    def fake_package_dir_exists(self: Path) -> bool:
        """Pretend the package directory exists so the flow reaches config files."""
        if self == expected_package_dir:
            return True
        return real_exists(self)

    mocker.patch.object(Path, "exists", fake_package_dir_exists)
    success, message = run_scenario("config_missing")
    assert success is False
    assert "Expected config file" in message
