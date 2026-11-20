"""module."""

from pathlib import Path

from pyrig_fixtures.rig.configs.fixtures.config import FixturesConfigConfigFile
from pyrig_fixtures.rig.tests import conftest


class TestFixturesConfigConfigFile:
    """Test class."""

    def test_content(self) -> None:
        """Test method."""
        assert (
            FixturesConfigConfigFile.I.plugin_definition()
            in FixturesConfigConfigFile.I.content()
        )

    def test_copy_module(self) -> None:
        """Test method."""
        assert FixturesConfigConfigFile.I.copy_module() is conftest

    def test_is_correct(self) -> None:
        """Test method."""
        assert FixturesConfigConfigFile.I.is_correct()

    def test_package_root(self) -> None:
        """Test method."""
        assert FixturesConfigConfigFile.I.package_root() == Path("tests")

    def test_parent_path(self) -> None:
        """Test method."""
        assert FixturesConfigConfigFile.I.parent_path() == Path("tests")

    def test_plugin_definition(self) -> None:
        """Test method."""
        assert (
            FixturesConfigConfigFile.I.plugin_definition()
            == f'pytest_plugins = ["{conftest.__name__}"]'
        )

    def test_stem(self) -> None:
        """Test method."""
        assert FixturesConfigConfigFile.I.stem() == "conftest"
