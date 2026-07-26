"""Shared pytest fixtures for creating temporary modules and packages.

Provides callables that build real Python modules and packages on disk (with
the appropriate `__init__.py` hierarchy) and import them, for tests that need
live module objects to introspect.
"""

from collections.abc import Callable
from contextlib import chdir
from pathlib import Path
from types import ModuleType

import pytest
from pyrig.core.introspection.modules import (
    import_module_with_file_fallback,
)
from pyrig.core.introspection.packages import (
    make_package_dir,
)
from pyrig.core.introspection.paths import path_as_module_name


@pytest.fixture
def create_module() -> Callable[[Path], ModuleType]:
    """Return a callable that creates and imports an empty Python module.

    Returns:
        A callable that creates an empty module file and imports it,
        initializing any missing parent directories as a package hierarchy
        first.
    """

    def create(path: Path) -> ModuleType:
        """Create an empty module file at `path` and import it.

        Args:
            path: Path to the module file, relative to the current working
                directory. Missing parent directories are created and given
                `__init__.py` files up to the current working directory.
                The imported module's dotted name is derived from this path.

        Returns:
            The imported module, empty of any definitions.
        """
        make_package_dir(path.parent, root=Path(), content="")
        path.touch()
        return import_module_with_file_fallback(path, name=path_as_module_name(path))

    return create


@pytest.fixture
def create_package() -> Callable[[Path], ModuleType]:
    """Return a callable that creates and imports an empty Python package.

    Returns:
        A callable that creates a directory tree as an empty package
        hierarchy and imports the deepest package.
    """

    def create(path: Path) -> ModuleType:
        """Create an empty package directory at `path` and import it.

        Args:
            path: Path to the package directory, relative to the current
                working directory. `path` and every ancestor directory up to
                the current working directory are created and given
                `__init__.py` files. The imported package's dotted name is
                derived from this path.

        Returns:
            The imported package, empty of any definitions.
        """
        make_package_dir(path, root=Path(), content="")
        return import_module_with_file_fallback(path, name=path_as_module_name(path))

    return create


@pytest.fixture
def create_source_package(
    tmp_source_root_path: Path,
    create_package: Callable[[Path], ModuleType],
) -> Callable[[Path], ModuleType]:
    """Return a callable that creates and imports a package under the source root.

    Args:
        tmp_source_root_path: Temporary source root directory that paths
            passed to the returned callable are resolved against.
        create_package: Fixture that creates and imports a package.

    Returns:
        A callable that creates an empty package under the temporary source
        root and imports it.
    """

    def create(path: Path) -> ModuleType:
        """Create an empty package at `path` under the source root and import it.

        Args:
            path: Path to the package directory, relative to the temporary
                source root directory.

        Returns:
            The imported package, empty of any definitions.
        """
        with chdir(tmp_source_root_path):
            return create_package(path)

    return create
