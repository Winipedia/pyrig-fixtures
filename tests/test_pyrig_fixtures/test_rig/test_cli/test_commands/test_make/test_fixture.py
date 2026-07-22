"""module."""

from collections.abc import Callable, Iterable
from contextlib import chdir
from pathlib import Path
from types import FunctionType

from pyrig.core.subprocesses import Args
from pyrig_runtime.core.strings import snake_to_kebab_case

from pyrig_fixtures.rig.cli import fixture
from pyrig_fixtures.rig.cli.commands.make.fixture import make_fixture


def test_fixture(
    command_calls_function: Callable[[FunctionType, FunctionType, Iterable[str]], bool],
) -> None:
    """Test function."""
    result = Args(
        *["pyrig", "mk", snake_to_kebab_case(fixture.__name__), "--help"],
    ).run(check=False)
    assert result.returncode == 0

    assert command_calls_function(fixture, make_fixture, ["my-new-fixture"])


def test_make_fixture(tmp_path: Path) -> None:
    """Test function."""
    project_path = tmp_path / "my-project"
    project_path.mkdir()

    with chdir(project_path):
        # create a new subcommand
        make_fixture("my-new-fixture")

        # check if the file was created and contains the expected content
        fixtures_file = (
            project_path
            / "src"
            / "my_project"
            / "rig"
            / "tests"
            / "fixtures"
            / "fixtures.py"
        )
        assert fixtures_file.exists(), f"{fixtures_file} does not exist"

        content = fixtures_file.read_text()
        assert "def my_new_fixture() -> None:" in content
        assert "@pytest.fixture" in content
        assert "import pytest" in content
        assert content.endswith("\n")
        assert '"""\n\nimport pytest' in content
        assert "pytest\n\n\n@pytest.fixture" in content

        make_fixture("another-fixture")
        content = fixtures_file.read_text()
        assert "def another_fixture() -> None:" in content
        assert content.count("@pytest.fixture") == 2  # noqa: PLR2004
        assert content.count("import pytest") == 1
        assert content.endswith("\n")
        assert '"""\n\nimport pytest' in content
        assert "pytest\n\n\n@pytest.fixture" in content
