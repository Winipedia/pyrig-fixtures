"""Shared pytest fixtures for testing the project's CLI commands.

Provides helpers that check whether a CLI command is registered and
reachable, and whether a command delegates to its expected implementation
function.
"""

from collections.abc import Callable, Iterable
from types import FunctionType

import pytest
from pyrig.rig.tools.packages.manager import PackageManager
from pyrig_runtime.core.strings import snake_to_kebab_case
from pyrig_runtime.rig.cli.cli import CLI
from pytest_mock import MockerFixture
from typer.testing import CliRunner


@pytest.fixture
def command_calls_function(
    mocker: MockerFixture,
) -> Callable[[FunctionType, FunctionType, Iterable[str]], bool]:
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

    def check(
        cmd: FunctionType,
        function: FunctionType,
        args: Iterable[str],
    ) -> bool:
        """Run `cmd` and return True if it calls `function` exactly once."""
        mock = mocker.patch(function.__module__ + "." + function.__name__)
        app = CLI.I.app()
        app.command()(cmd)
        CliRunner().invoke(app, [snake_to_kebab_case(cmd.__name__), *(args or [])])
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
