"""Test module."""

from collections.abc import Callable, Iterable
from types import FunctionType

from pyrig_fixtures.rig.cli.commands.fixture import make_fixture
from pyrig_fixtures.rig.cli.subcommands import fixture


def test_fixture(
    command_calls_function: Callable[[FunctionType, FunctionType, Iterable[str]], bool],
    command_works: Callable[[FunctionType], bool],
) -> None:
    """Test function."""
    assert command_works(fixture)
    assert command_calls_function(fixture, make_fixture, ["my-new-fixture"])
