"""Shared pytest fixtures for testing `ConfigFile` subclasses in isolation.

Provides a factory that redirects a `ConfigFile` subclass's file operations
to pytest's `tmp_path` so tests never touch real project files.
"""

from collections.abc import Callable
from contextlib import chdir
from pathlib import Path
from typing import Any

import pytest
from pyrig.rig.configs.base.config_file import ConfigFile


@pytest.fixture
def config_file_factory[T: ConfigFile[dict[str, Any] | list[Any]]](
    tmp_path: Path,
) -> Callable[[type[T]], type[T]]:
    """Return a factory that wraps a `ConfigFile` subclass for isolated testing.

    Each call to the factory dynamically creates a new wrapping subclass, so
    it may be invoked with a different `ConfigFile` subclass any number of
    times within the same test.

    Args:
        tmp_path: Pytest's per-test temporary directory.

    Returns:
        A callable that accepts a `ConfigFile` subclass and returns a
        test-safe subclass with `tmp_path`-based file operations.
    """

    def _make_test_config(
        base_class: type[T],
    ) -> type[T]:
        """Wrap `base_class` with `tmp_path`-redirected file operations.

        Args:
            base_class: The `ConfigFile` subclass to wrap.

        Returns:
            A subclass of `base_class` with all file paths redirected to
            `tmp_path`.
        """

        class TestConfigFile(base_class):  # ty: ignore[unsupported-base]
            """Subclass of `base_class` with every file operation under `tmp_path`."""

            def path(self) -> Path:
                """Return the config file path, relocated under `tmp_path`.

                Returns:
                    The path from the parent implementation, guaranteed to
                    resolve to a location under `tmp_path`.
                """
                path = super().path()
                if not (path.is_relative_to(tmp_path) or Path.cwd() == tmp_path):
                    path = tmp_path / path
                return path

            def _dump(self, configs: dict[str, Any] | list[Any]) -> None:
                """Write the config from within `tmp_path`, isolating real files."""
                with chdir(tmp_path):
                    super()._dump(configs)

            def _load(self) -> dict[str, Any] | list[Any]:
                """Load the config from within `tmp_path`, isolating real files."""
                with chdir(tmp_path):
                    return super()._load()

            def create_file(self) -> None:
                """Create the file from within `tmp_path`, isolating real files."""
                with chdir(tmp_path):
                    super().create_file()

        return TestConfigFile  # ty:ignore[invalid-return-type]

    return _make_test_config
