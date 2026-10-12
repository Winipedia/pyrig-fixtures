"""Test module."""

from collections.abc import Callable, Iterable
from types import FunctionType

from pyrig_fixtures.rig.cli.commands.fixture import make_fixture
from pyrig_fixtures.rig.cli.subcommands import fixture


def test_command_works(command_works: Callable[[FunctionType], bool]) -> None:
    """Test function."""
    assert command_works(fixture)


def test_command_calls_function(
    command_calls_function: Callable[[FunctionType, FunctionType, Iterable[str]], bool],
) -> None:
    """Test function."""
    assert command_calls_function(fixture, make_fixture, ["my-new-fixture"])
