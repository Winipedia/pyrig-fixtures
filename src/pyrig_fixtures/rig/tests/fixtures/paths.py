"""Fixtures for building a temporary project/source/package directory tree.

Provides an empty, disposable instance of this ecosystem's conventional src
layout (project root → source root → package root), so tests can exercise
path-sensitive logic without touching the real project on disk.
"""

from collections.abc import Callable
from pathlib import Path
from types import ModuleType

import pytest
from pyrig.rig.tools.packages.manager import PackageManager


@pytest.fixture
def tmp_package_root_path(
    tmp_project_root_path: Path,
    tmp_source_root_path: Path,
    create_source_package: Callable[[Path], ModuleType],
) -> tuple[Path, ModuleType]:
    """Provide the temporary package root, already created and imported as a package.

    Args:
        tmp_project_root_path: Temporary project root directory.
        tmp_source_root_path: Temporary source root directory.
        create_source_package: Callable that creates and imports a package at
            a path relative to the temporary source root.

    Returns:
        Tuple of `(path, package)`: the package root directory nested inside
        the temporary source root, and its imported package module.
    """
    path = tmp_project_root_path / PackageManager.I.package_root()

    package = create_source_package(path.relative_to(tmp_source_root_path))
    return path, package


@pytest.fixture
def tmp_project_root_path(tmp_path: Path) -> Path:
    """Provide a temporary project root directory named after the current project.

    Args:
        tmp_path: Pytest's per-test temporary directory.

    Returns:
        Path to the temporary project root directory, already created on disk.
    """
    path = tmp_path / PackageManager.I.project_name()
    path.mkdir()
    return path


@pytest.fixture
def tmp_source_root_path(tmp_project_root_path: Path) -> Path:
    """Provide a temporary source root directory nested inside the project root.

    Args:
        tmp_project_root_path: Temporary project root directory.

    Returns:
        Path to the temporary source root directory, already created on disk.
    """
    path = tmp_project_root_path / PackageManager.I.source_root()
    path.mkdir()
    return path
