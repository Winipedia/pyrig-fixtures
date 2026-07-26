"""Shared pytest fixtures for gating tests by platform and Python version.

Provides session-scoped predicates for the current OS and interpreter version,
used to restrict environment-sensitive tests to a canonical CI environment
while still running them locally.
"""

import platform
from collections.abc import Callable

import pytest
from pyrig.rig.configs.pyproject import PyprojectConfigFile
from pyrig.rig.tools.version_control.remote.controller import (
    RemoteVersionController,
)


@pytest.fixture(scope="session")
def on_latest_python_version(on_python_version: Callable[[str], bool]) -> bool:
    """Return whether the running Python version matches the latest stable release.

    Args:
        on_python_version: Callable that checks whether a given version string
            exactly matches the running Python version.

    Returns:
        True if the current Python micro version matches the latest stable
        release.
    """
    latest_version = PyprojectConfigFile.I.latest_python_version("micro")
    return on_python_version(str(latest_version))


@pytest.fixture(scope="session")
def on_linux(on_platform: Callable[[str], bool]) -> bool:
    """Return whether the current system is Linux.

    Args:
        on_platform: Callable that checks whether a given platform name
            exactly matches the current system platform.

    Returns:
        True if the system is Linux.
    """
    return on_platform("Linux")


@pytest.fixture(scope="session")
def on_linux_and_latest_python_version(
    *,
    on_linux: bool,
    on_latest_python_version: bool,
) -> bool:
    """Return whether the current environment is Linux with the latest Python version.

    Args:
        on_linux: Whether the current system is Linux.
        on_latest_python_version: Whether the running Python version matches
            the latest stable release.

    Returns:
        True if both conditions are met.
    """
    return on_linux and on_latest_python_version


@pytest.fixture(scope="session")
def on_linux_and_latest_python_version_or_not_in_ci(
    *,
    on_linux_and_latest_python_version: bool,
) -> bool:
    """Return whether tests that require a canonical environment should run.

    Args:
        on_linux_and_latest_python_version: Whether the environment is Linux
            with the latest Python version.

    Returns:
        True if the environment is Linux with the latest Python version, or
        if not currently running inside GitHub Actions.
    """
    return (
        on_linux_and_latest_python_version
    ) or not RemoteVersionController.I.running_in_ci()


@pytest.fixture(scope="session")
def on_platform() -> Callable[[str], bool]:
    """Check whether the current system platform exactly matches a given name.

    Returns:
        A callable `(platform_name) -> bool` that returns `True` only when
        `platform_name` exactly equals `platform.system()` (e.g., `"Linux"`,
        `"Windows"`, `"Darwin"`).
    """

    def check(platform_name: str) -> bool:
        return platform.system() == platform_name

    return check


@pytest.fixture(scope="session")
def on_python_version() -> Callable[[str], bool]:
    """Check whether the current Python version exactly matches a given version string.

    Returns:
        A callable `(version) -> bool` that returns `True` only when `version`
        exactly equals `platform.python_version()` (e.g., `"3.13.2"`).
    """

    def check(version: str) -> bool:
        return platform.python_version() == version

    return check
