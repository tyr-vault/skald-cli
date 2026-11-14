"""Initialize Skald workspace."""

from __future__ import annotations

from pathlib import Path

from skald.core.config import SkaldConfig, write_default_config
from skald.storage.database import get_session_factory
from skald.utils.filesystem import ensure_dir


def init_workspace(config: SkaldConfig, config_path: Path) -> None:
    write_default_config(config_path)
    ensure_dir(config.workspace.path)
    ensure_dir(config.content.output_directory)
    ensure_dir(config.workspace.path / "artifacts")
    ensure_dir(config.workspace.path / "features")
    ensure_dir(config_path.parent)
    get_session_factory(config.storage.database)
