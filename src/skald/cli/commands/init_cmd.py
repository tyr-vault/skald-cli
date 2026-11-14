"""skald init command."""

from __future__ import annotations

from pathlib import Path

import typer
from rich.console import Console

from skald.application.init_workspace import init_workspace
from skald.core.config import config_file_path, resolve_config

console = Console()


def init(
    config_path: Path | None = typer.Option(
        None,
        "--config",
        help="Path to config file (default ~/.config/devlog/config.yaml)",
    ),
) -> None:
    """Initialize local Skald workspace, config, and database."""
    target = (config_path or config_file_path()).expanduser()
    cfg = resolve_config(target if config_path else None)
    init_workspace(cfg, target)
    console.print("[green]Skald workspace initialized[/green]")
    console.print(f"Config: {target}")
    console.print(f"Database: {cfg.storage.database}")
    console.print(f"Workspace: {cfg.workspace.path}")
