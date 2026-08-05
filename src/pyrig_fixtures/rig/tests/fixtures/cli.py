"""Shared pytest fixtures for testing the project's CLI commands.

Provides helpers that check whether a CLI command is registered and
reachable, and whether a command delegates to its expected implementation
function.
"""

from collections.abc import Callable, Iterable
from types import FunctionType

import pytest
import typer
from pyrig.core.subprocesses import Args
from pyrig.rig.tools.packages.manager import PackageManager
from pyrig_runtime.core.strings import snake_to_kebab_case
from pytest_mock import MockerFixture
from typer.testing import CliRunner


@pytest.fixture
def command_calls_function(
    mocker: MockerFixture,
) -> Callable[[FunctionType, FunctionType, Iterable[str]], bool]:
    """Return a callable that verifies a CLI command delegates to a function.

    The returned callable registers `cmd` on a freshly built CLI app, patches
    `function` where it is defined, invokes `cmd` through the CLI with
    `args`, and reports whether the patch was called exactly once. Whether
    the invocation itself succeeds is not checked.
    Adds a second dummy command to prevent the only one command from being treated
    as the default command.

    Args:
        mocker: pytest-mock fixture used to patch `function`.

    Returns:
        A callable `(cmd, function, args) -> bool` that returns `True` if
        `function` is called exactly once while `cmd` runs with `args`,
        `False` otherwise.
    """

    def check(
        cmd: FunctionType,
        function: FunctionType,
        args: Iterable[str],
    ) -> bool:
        """Run `cmd` with `args`; return whether `function` was called exactly once."""
        mock = mocker.patch(function.__module__ + "." + function.__name__)
        app = typer.Typer(name="some-app", no_args_is_help=True)
        app.command()(lambda: None)
        app.command()(cmd)
        CliRunner().invoke(app, [snake_to_kebab_case(cmd.__name__), *(args or [])])
        return mock.call_count == 1

    return check


@pytest.fixture
def command_works() -> Callable[[FunctionType], bool]:
    """Return a callable that verifies a CLI command is registered and reachable.

    The returned callable runs `cmd` as a subcommand of the project's CLI
    with `--help` and checks whether its kebab-case name appears in stdout.

    Returns:
        A callable `(cmd) -> bool` that returns `True` if `cmd`'s kebab-case
        name appears in the `--help` output, `False` otherwise.

    Raises:
        subprocess.CalledProcessError: If invoking `cmd` with `--help` exits
            with a non-zero status, for example because `cmd` is not
            registered as a subcommand of the project's CLI.
    """

    def check(cmd: FunctionType) -> bool:
        """Run `cmd` with `--help` and return whether its name appears in stdout."""
        args = Args(
            PackageManager.I.project_name(),
            snake_to_kebab_case(cmd.__name__),
            "--help",
        )
        completed_process = args.run()
        stdout = completed_process.stdout
        name = cmd.__name__.replace("_", "-")
        return name in stdout

    return check
