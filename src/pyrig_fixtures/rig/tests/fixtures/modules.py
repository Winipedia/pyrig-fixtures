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
    """Return a callable that creates a Python module at a given path.

    The returned function ensures the parent directory is a proper package
    hierarchy (adding `__init__.py` files up to the current working
    directory), touches the module file, and imports it.

    Returns:
        A callable `(path) -> ModuleType` that creates and imports an empty
        module at `path`.
    """

    def create(path: Path) -> ModuleType:
        """Create and import an empty module at `path`."""
        make_package_dir(path.parent, root=Path(), content="")
        path.touch()
        return import_module_with_file_fallback(path, name=path_as_module_name(path))

    return create


@pytest.fixture
def create_package() -> Callable[[Path], ModuleType]:
    """Return a callable that creates a Python package at a given path.

    The returned function initializes the full directory tree as a package
    hierarchy by adding `__init__.py` files up to the current working
    directory, then imports and returns the package.

    Returns:
        A callable `(path) -> ModuleType` that creates and imports an empty
        package at `path`.
    """

    def create(path: Path) -> ModuleType:
        """Create and import an empty package at `path`."""
        make_package_dir(path, root=Path(), content="")
        return import_module_with_file_fallback(path, name=path_as_module_name(path))

    return create


@pytest.fixture
def create_source_package(
    tmp_source_root_path: Path, create_package: Callable[[Path], ModuleType]
) -> Callable[[Path], ModuleType]:
    """Return a callable that creates a Python package under the temporary source root.

    Args:
        tmp_source_root_path: Temporary source root directory.
        create_package: Fixture that creates and imports a package.

    Returns:
        A callable `(path) -> ModuleType` that creates and imports an empty
        package at `path` relative to the temporary source root.
    """

    def create(path: Path) -> ModuleType:
        """Create and import an empty package at `path` relative to the source root."""
        with chdir(tmp_source_root_path):
            return create_package(path)

    return create
