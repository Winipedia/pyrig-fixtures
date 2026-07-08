"""Shared pytest fixtures for testing the project's CLI commands.

Provides helpers that check whether a CLI command is registered and
reachable, and whether a command delegates to its expected implementation
function.
"""

from collections.abc import Callable
from types import FunctionType

import pytest
from pyrig.rig.tools.package_manager import PackageManager
from pytest_mock import MockerFixture


@pytest.fixture
def command_calls_function(
    mocker: MockerFixture,
) -> Callable[[FunctionType, FunctionType], bool]:
    """Return a callable that verifies a CLI command delegates to the expected function.

    The returned function patches the target function by its fully qualified
    name, invokes the command, and checks whether the patch was called
    exactly once.

    Args:
        mocker: pytest-mock fixture for patching.

    Returns:
        A callable `(cmd, function) -> bool` that returns True if `cmd` calls
        `function` exactly once, False otherwise.
    """

    def check(cmd: FunctionType, function: FunctionType) -> bool:
        """Run `cmd` and return True if it calls `function` exactly once."""
        mock = mocker.patch(function.__module__ + "." + function.__name__)
        cmd()
        return mock.call_count == 1

    return check


@pytest.fixture
def command_works() -> Callable[[FunctionType], bool]:
    """Return a callable that verifies a CLI command is registered and executable.

    The returned function runs the command with `--help` and checks whether
    the command executes successfully and its name appears in stdout.

    Returns:
        A callable `(cmd) -> bool` that accepts a CLI function and returns
        True if it is reachable and produces help output, False otherwise.
    """

    def check(cmd: FunctionType) -> bool:
        """Run `cmd` with `--help` and return whether its name appears in stdout."""
        args = PackageManager.I.project_cmd_args("--help", cmd=cmd)
        completed_process = args.run()
        stdout = completed_process.stdout
        name = cmd.__name__.replace("_", "-")
        return name in stdout

    return check
