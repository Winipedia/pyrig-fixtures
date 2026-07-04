"""test module."""

from collections.abc import Callable
from types import FunctionType

from pyrig_runtime.rig.cli.commands.version import project_version
from pyrig_runtime.rig.cli.shared_subcommands import version


def test_command_works(command_works: Callable[[FunctionType], bool]) -> None:
    """Test function."""
    assert command_works(version)


def test_command_calls_function(
    command_calls_function: Callable[[FunctionType, FunctionType], bool],
) -> None:
    """Test function."""
    assert command_calls_function(version, project_version)
