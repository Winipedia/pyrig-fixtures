"""Package initialization."""

import typer
from pyrig.rig.cli.subcommands import mk


@mk.command()
def fixture(
    name: str = typer.Argument(help="Name of the fixture to create."),
) -> None:
    """Scaffold a new pytest fixture stub in the project's shared fixtures module.

    Appends an `@pytest.fixture`-decorated function stub to the shared fixtures
    module. The file is created if it does not already exist. If `import pytest`
    is not already present in the module, it is inserted automatically.

    The name is normalized from kebab-case to snake_case so it forms a valid
    Python identifier (e.g. `my-new-fixture` becomes `my_new_fixture`).

    Example:
        $ uv run pyrig mk fixture my-fixture
    """
    from pyrig_fixtures.rig.cli.commands.make.fixture import (  # noqa: PLC0415
        make_fixture,
    )

    make_fixture(name)
