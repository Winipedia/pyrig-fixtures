"""test module."""

from collections.abc import Callable
from typing import Any

from pyrig_runtime.rig.cli.commands.version import project_version
from pyrig_runtime.rig.cli.shared_subcommands import version


def test_command_works(command_works: Callable[[Callable[..., Any]], None]) -> None:
    """Test function."""
    command_works(version)


def test_command_calls_function(
    command_calls_function: Callable[[Callable[..., Any], Callable[..., Any]], None],
) -> None:
    """Test function."""
    command_calls_function(version, project_version)
