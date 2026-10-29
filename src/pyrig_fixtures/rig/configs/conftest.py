"""Configuration for the generated `tests/conftest.py` file.

Manages a conftest file that registers pyrig_fixtures' own conftest module as
a pytest plugin, giving the target project access to it without an explicit
import in each test file.
"""

from pathlib import Path
from types import ModuleType
from typing import override

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

    @override
    def content(self) -> str:
        """Return the generated `conftest.py` file's content.

        Returns:
            The module docstring of `pyrig_fixtures.rig.tests.conftest` followed
            by a `pytest_plugins` assignment that registers that module as a
            pytest plugin.
        """
        return f"{super().content()}\n{self.plugin_definition()}\n"

    @override
    def copy_module(self) -> ModuleType:
        """Return the `pyrig_fixtures.rig.tests.conftest` module."""
        return conftest

    @override
    def is_correct(self) -> bool:
        """Return whether the conftest module is already registered as a pytest plugin.

        Returns:
            `True` if the file currently on disk contains
            `pyrig_fixtures.rig.tests.conftest`'s dotted name.
        """
        return conftest.__name__ in self.read_content()

    @override
    def parent_path(self) -> Path:
        """Return the tests package root as the generated file's parent directory."""
        return self.package_root()

    @override
    def stem(self) -> str:
        """Return the filename stem for the generated file.

        Returns:
            `'conftest'`
        """
        return "conftest"

    @override
    def package_root(self) -> Path:
        """Return the tests package root rather than the source package root."""
        return ProjectTester.I.package_root()

    def plugin_definition(self) -> str:
        """Return the `pytest_plugins` assignment line for the generated file.

        Returns:
            `'pytest_plugins = ["pyrig_fixtures.rig.tests.conftest"]'`.
        """
        return f'pytest_plugins = ["{conftest.__name__}"]'
