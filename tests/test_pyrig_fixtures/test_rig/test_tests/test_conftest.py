"""module for the following module path (maybe truncated).

tests.test_pyrig.test_testing.test_tests.test_conftest
"""

from pyrig_fixtures.rig.tests import conftest
from pyrig_fixtures.rig.tests.fixtures import fixtures


def test_pytest_plugins() -> None:
    """Test function."""
    plugins = conftest.pytest_plugins
    assert fixtures.__name__ in plugins
