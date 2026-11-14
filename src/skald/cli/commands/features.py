"""skald features commands."""

from __future__ import annotations

import typer
from rich.console import Console

from skald.application import features as feature_uc
from skald.core.config import is_initialized
from skald.core.container import AppContext, build_context
from skald.core.exceptions import NotInitializedError

app = typer.Typer(help="List and export discovered features.")
console = Console()


def _ctx() -> AppContext:
    if not is_initialized():
        raise NotInitializedError("Run `skald init` first.")
    return build_context()


@app.command("list")
def list_features() -> None:
    """List discovered features."""
    ctx = _ctx()
    items = feature_uc.list_features(ctx)
    if not items:
        console.print("No features yet. Run `skald analyze`.")
        return
    for f in items:
        console.print(f"{f.id}  [{f.confidence:.2f}]  {f.title}")


@app.command("show")
def show_feature(feature_id: str = typer.Argument(...)) -> None:
    """Show feature details."""
    ctx = _ctx()
    f = feature_uc.get_feature(ctx, feature_id)
    console.print(f"[bold]{f.title}[/bold]")
    console.print(f"Summary: {f.summary}")
    console.print(f"Confidence: {f.confidence}  Status: {f.status}")
    console.print(f"Commits: {', '.join(s[:8] for s in f.related_commits)}")
    console.print(f"Files: {len(f.related_files)}")


@app.command("export")
def export_feature(
    feature_id: str = typer.Argument(...),
    format: str = typer.Option("yaml", "--format", help="Export format"),
) -> None:
    """Export feature metadata."""
    ctx = _ctx()
    path = feature_uc.export_feature(ctx, feature_id, format)
    console.print(f"[green]Exported to[/green] {path}")
