"""Typer application root."""

from __future__ import annotations

import typer

from skald.cli.commands import analyze, content, features, init_cmd, report, scan

app = typer.Typer(
    name="skald",
    help="Skald — turn engineering activity into reusable technical knowledge.",
    no_args_is_help=True,
)
app.command("init")(init_cmd.init)
app.add_typer(scan.app, name="scan")
app.command("analyze")(analyze.analyze)
app.add_typer(features.app, name="features")
app.add_typer(content.app, name="content")
app.command("report")(report.report)
