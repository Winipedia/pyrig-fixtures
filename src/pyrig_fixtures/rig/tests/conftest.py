"""Pytest configuration for automatic fixture discovery across dependent packages.

Registers every fixture module in this package's fixtures package, and in the
equivalent fixtures package of every installed package that depends on it, as
a pytest plugin. This makes all discovered fixtures available in every test
module without explicit imports.
"""

from itertools import chain
from pathlib import Path

from pyrig.core.introspection.paths import package_dir_path, path_as_module_name
from pyrig_runtime.core.dependencies.discovery import (
    discover_equivalent_modules_across_dependencies,
)

from pyrig_fixtures.rig.tests import fixtures

module_names: list[str] = []
for package in chain(
    (fixtures,),
    discover_equivalent_modules_across_dependencies(fixtures),
):
    package_name = package.__name__
    package_path = package_dir_path(package)

    for path in package_path.rglob("*.py"):
        if path.name == "__init__.py":
            continue

        module_name_as_path = Path(package_name) / path.relative_to(package_path)

        module_name = path_as_module_name(module_name_as_path)

        module_names.append(module_name)

pytest_plugins = tuple(module_names)
