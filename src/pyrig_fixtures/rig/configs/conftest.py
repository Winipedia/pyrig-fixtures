"""Configuration for the generated `tests/conftest.py` file.

Manages a conftest file that registers pyrig_fixtures' own conftest module as
a pytest plugin, giving the target project access to it without an explicit
import in each test file.
"""

from pathlib import Path
from types import ModuleType

from pyrig.rig.configs.base.copy_module import CopyModuleDocstringConfigFile
from pyrig.rig.tools.testing.project import ProjectTester

from pyrig_fixtures.rig.tests import conftest


class ConftestConfigFile(CopyModuleDocstringConfigFile):
    """The `tests/conftest.py` config file, generated for the target project.

    The generated file has two parts: the module-level docstring of
    `pyrig_fixtures.rig.tests.conftest` as its own module docstring, followed
    by a `pytest_plugins` assignment that registers that module as a pytest
    plugin, giving the target project automatic access to it without needing an
    explicit import in each test file.
    """

    def is_correct(self) -> bool:
        """Return whether the conftest module is already registered as a pytest plugin.

        Returns:
            `True` if `pyrig_fixtures.rig.tests.conftest`'s dotted name is
            listed in the `pytest_plugins` list of the file currently on disk.
        """
        return conftest.__name__ in getattr(self.module(), "pytest_plugins", [])

    def content(self) -> str:
        """Return the generated `conftest.py` file's content.

        Returns:
            The module docstring of `pyrig_fixtures.rig.tests.conftest` followed
            by a `pytest_plugins` assignment that registers that module as a
            pytest plugin.
        """
        return f"{super().content()}\n{self.plugin_definition()}\n"

    def copy_module(self) -> ModuleType:
        """Return the `pyrig_fixtures.rig.tests.conftest` module."""
        return conftest

    def parent_path(self) -> Path:
        """Return the tests package root as the generated file's parent directory."""
        return self.package_root()

    def package_root(self) -> Path:
        """Return the tests package root rather than the source package root."""
        return ProjectTester.I.package_root()

    def stem(self) -> str:
        """Return the filename stem for the generated file.

        Returns:
            `'conftest'`
        """
        return "conftest"

    def plugin_definition(self) -> str:
        """Return the `pytest_plugins` assignment line for the generated file.

        Returns:
            `'pytest_plugins = ["pyrig_fixtures.rig.tests.conftest"]'`.
        """
        return f'pytest_plugins = ["{conftest.__name__}"]'
