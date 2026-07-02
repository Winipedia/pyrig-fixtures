"""Scaffolding for shared pytest fixtures in a pyrig-managed project."""

import pytest
from pyrig.rig.configs.base.copy_module_docstring import (
    CopyModuleDocstringConfigFile,
)
from pyrig_runtime.core.strings import kebab_to_snake_case

from pyrig_fixtures.rig.tests.fixtures import fixtures


def make_fixture(name: str) -> None:
    """Scaffold a new pytest fixture in the project's shared fixtures module.

    Ensures the shared fixtures module exists, then appends a new
    `@pytest.fixture`-decorated function with the given name. If
    `import pytest` is not already present in the module, it is added
    before the new fixture.

    The name is normalized from kebab-case to snake_case so it forms a
    valid Python identifier (e.g. `"my-new-fixture"` becomes
    `"my_new_fixture"`).

    Args:
        name: Name of the fixture in kebab-case or snake_case.
    """
    config_file = CopyModuleDocstringConfigFile.generate_subclass(fixtures)()
    config_file.validate()
    content = config_file.read_content()

    name = kebab_to_snake_case(name)
    pytest_import = f"import {pytest.__name__}"
    # checking with splitlines to avoid substring matches, like import pytest_mock
    if pytest_import not in content.splitlines():
        content += f"""
{pytest_import}
"""

    content += f'''

@{pytest.__name__}.{pytest.fixture.__name__}
def {name}() -> None:
    """This is a test fixture."""
'''

    config_file.write_content(content)
