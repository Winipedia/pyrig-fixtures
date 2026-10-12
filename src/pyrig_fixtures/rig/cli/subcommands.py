"""Project-specific CLI commands.

Functions defined directly in this module are registered as top-level CLI
commands. Module-level `typer.Typer` instances are registered as command
groups, with each group's name derived from the kebab-case form of the
variable name.
"""

from typing import Annotated

import typer


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
        $ uv run pyrig-fixtures fixture my-fixture
        ```
    """
    from pyrig_fixtures.rig.cli.commands.fixture import (  # noqa: PLC0415
        make_fixture,
    )

    make_fixture(name)
