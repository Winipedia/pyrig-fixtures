"""CLI commands that pyrig-fixtures adds to the `mk` scaffolding command group."""

from typing import Annotated

import typer
from pyrig.rig.cli.subcommands import mk


@mk.command()
def fixture(
    name: Annotated[str, typer.Argument(help="Name of the fixture to create.")],
) -> None:
    """Scaffold a new pytest fixture stub in the project's shared fixtures module.

    Appends an `@pytest.fixture`-decorated function stub to the shared fixtures
    module. The file is created if it does not already exist. If `import pytest`
    is not already present in the module, it is inserted automatically.

    Args:
        name: Name of the fixture to create. Accepts kebab-case or snake_case;
            kebab-case is normalized to snake_case to form a valid identifier
            (e.g. `my-new-fixture` becomes `my_new_fixture`).

    Example:
        ```
        $ uv run pyrig mk fixture my-fixture
        ```
    """
    from pyrig_fixtures.rig.cli.commands.make.fixture import (  # noqa: PLC0415
        make_fixture,
    )

    make_fixture(name)
