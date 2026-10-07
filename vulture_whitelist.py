"""Explicit references for reviewed dead code false positives."""

from pyrig.rig.configs.base.config_file import ConfigFile
from pyrig.rig.configs.base.copy_module import CopyModuleConfigFile
from pyrig.rig.configs.base.string_ import StringConfigFile

from pyrig_fixtures.rig.configs.conftest import ConftestConfigFile
from pyrig_fixtures.rig.tests.fixtures.cli import (
    command_calls_function,
    command_works,
)
from pyrig_fixtures.rig.tests.fixtures.configs import config_file_factory
from pyrig_fixtures.rig.tests.fixtures.environment import (
    on_linux_and_latest_python_version_or_not_in_ci,
)
from pyrig_fixtures.rig.tests.fixtures.fixtures import pytest_addoption
from pyrig_fixtures.rig.tests.fixtures.modules import create_module
from pyrig_fixtures.rig.tests.fixtures.paths import tmp_package_root_path

_CONFIG_FILE_OVERRIDES = (
    ConfigFile.is_correct,
    ConfigFile.parent_path,
    ConfigFile.stem,
    CopyModuleConfigFile.copy_module,
    StringConfigFile.content,
)
_CONFIG_FILES = (ConftestConfigFile,)
_PYTEST_FIXTURES = (
    command_calls_function,
    command_works,
    config_file_factory,
    create_module,
    on_linux_and_latest_python_version_or_not_in_ci,
    pytest_addoption,
    tmp_package_root_path,
)
