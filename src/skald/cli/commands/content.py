"""skald content commands."""

from __future__ import annotations

import typer
from rich.console import Console

from skald.application.content import draft_content
from skald.core.config import is_initialized
from skald.core.container import build_context
from skald.core.exceptions import NotInitializedError

app = typer.Typer(help="Generate content drafts from features.")
console = Console()


@app.command("draft")
def draft(
    feature_id: str = typer.Argument(...),
    format: str = typer.Option("article", "--format", help="article|learning-note|linkedin"),
) -> None:
    """Generate a Markdown draft for a feature."""
    if not is_initialized():
        raise NotInitializedError("Run `skald init` first.")
    ctx = build_context()
    meta = draft_content(ctx, feature_id, format)
    console.print(f"[green]Draft written[/green] {meta.output_path}")
