"""test module."""

from collections.abc import Callable
from contextlib import chdir
from pathlib import Path
from typing import Any

import pytest
from pyrig.rig.configs.base.config_file import ConfigFile


@pytest.fixture
def sample_config_file(
    config_file_factory: Callable[
        [type[ConfigFile[dict[str, Any]]]], type[ConfigFile[dict[str, Any]]]
    ],
) -> type[ConfigFile[dict[str, Any]]]:
    """Create a sample config file class for testing the factory."""

    class SampleConfigFile(config_file_factory(ConfigFile)):  # ty: ignore[unsupported-base]
        """Sample config file for testing."""

        def parent_path(self) -> Path:
            """Get the parent path."""
            return Path()

        def stem(self) -> str:
            """Get the stem."""
            return "sample"

        def _load(self) -> dict[str, Any]:
            """Load the config."""
            super()._load()
            return {"key": "value"}

        def _dump(self, configs: dict[str, Any] | list[Any]) -> None:
            """Dump the config."""
            return super()._dump(configs)

        def extension(self) -> str:
            """Get the file extension."""
            return "test"

        def _configs(self) -> dict[str, Any]:
            """Get the configs."""
            return {"key": "value"}

    return SampleConfigFile


def test_config_file_factory(
    sample_config_file: type[ConfigFile[dict[str, Any]]], tmp_path: Path
) -> None:
    """Test that config_file_factory wraps path to use tmp_path."""
    assert issubclass(sample_config_file, ConfigFile)

    # The factory should wrap the path method to use tmp_path
    path = sample_config_file().path()

    # The path should be inside tmp_path
    assert str(path).startswith(str(tmp_path))

    # The path should have the correct extension
    assert path.suffix == ".test", f"Expected extension '.test', got {path.suffix}"

    assert path.name == "sample.test", (
        f"Expected filename 'sample.test', got {path.name}"
    )

    assert not path.exists()
    sample_config_file().validate()
    assert path.exists()

    path.unlink()
    assert not path.exists()

    with chdir(tmp_path):
        assert issubclass(sample_config_file, ConfigFile)
        path: Path = sample_config_file().path()
        assert not str(path).startswith(str(tmp_path))

        sample_config_file().validate()
        assert sample_config_file().is_correct()

        assert path.exists()
