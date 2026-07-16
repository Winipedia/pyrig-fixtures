"""module."""

from pathlib import Path

from pyrig_fixtures.rig.configs.conftest import ConftestConfigFile
from pyrig_fixtures.rig.tests import conftest


class TestConftestConfigFile:
    """Test class."""

    def test_package_root(self) -> None:
        """Test method."""
        assert ConftestConfigFile.I.package_root() == Path("tests")

    def test_is_correct(self) -> None:
        """Test method."""
        assert ConftestConfigFile.I.is_correct()

    def test_parent_path(self) -> None:
        """Test method."""
        assert ConftestConfigFile.I.parent_path() == Path("tests")

    def test_copy_module(self) -> None:
        """Test method."""
        assert ConftestConfigFile.I.copy_module() is conftest

    def test_plugin_definition(self) -> None:
        """Test method."""
        assert (
            ConftestConfigFile.I.plugin_definition()
            == f'pytest_plugins = ["{conftest.__name__}"]'
        )

    def test_stem(self) -> None:
        """Test method."""
        assert ConftestConfigFile.I.stem() == "conftest"

    def test_content(self) -> None:
        """Test method."""
        assert (
            ConftestConfigFile.I.plugin_definition() in ConftestConfigFile.I.content()
        )
