"""skald analyze command."""

from __future__ import annotations

import typer
from rich.console import Console

from skald.application.analyze import analyze_use_case
from skald.core.config import is_initialized
from skald.core.container import build_context
from skald.core.exceptions import NotInitializedError

console = Console()


def analyze(
    repository_id: str | None = typer.Option(None, "--repository-id", help="Limit to repository"),
) -> None:
    """Normalize data, group commits, extract knowledge, store features."""
    if not is_initialized():
        raise NotInitializedError("Run `skald init` first.")
    ctx = build_context()
    count = analyze_use_case(ctx, repository_id)
    console.print(f"[green]Discovered {count} feature(s)[/green]")
