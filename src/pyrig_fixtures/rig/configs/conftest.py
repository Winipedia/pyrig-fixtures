"""Configuration for the generated `tests/conftest.py` file.

Manages a conftest file that registers pyrig_fixtures' own conftest module as
a pytest plugin, giving the target project access to it without an explicit
import in each test file.
"""

from pathlib import Path
from types import ModuleType

from pyrig.rig.configs.base.copy_module_docstring import CopyModuleDocstringConfigFile
from pyrig.rig.tools.testers.project import ProjectTester

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
        """Return whether the generated conftest.py is considered valid.

        The file is valid if the conftest module name is registered in the
        `pytest_plugins` list of the file on disk.

        Returns:
            `True` if the conftest module name is present in the
            `pytest_plugins` list of the file on disk.
        """
        return conftest.__name__ in getattr(self.module(), "pytest_plugins", [])

    def lines(self) -> list[str]:
        """Return the content of the generated conftest.py as a list of lines.

        Extends the parent output (the conftest module's docstring) with the
        `pytest_plugins` assignment and a trailing blank line.

        Returns:
            Lines comprising the module docstring followed by the
            `pytest_plugins` assignment.
        """
        return [*super().lines(), self.plugin_definition(), ""]

    def copy_module(self) -> ModuleType:
        """Return the source module whose docstring is written to the generated file.

        Returns:
            `pyrig_fixtures.rig.tests.conftest`
        """
        return conftest

    def parent_path(self) -> Path:
        """Return the root directory of the tests package.

        Returns:
            Path to the tests package root, e.g. `Path("tests")`.
        """
        return self.package_root()

    def package_root(self) -> Path:
        """Override to return the root directory of the tests package."""
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
            String of the form `'pytest_plugins = ["<conftest_module_name>"]'`.
        """
        return f'pytest_plugins = ["{conftest.__name__}"]'
