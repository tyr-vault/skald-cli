"""skald report command."""

from __future__ import annotations

from rich.console import Console

from skald.application.report import render_report
from skald.core.config import is_initialized
from skald.core.container import build_context
from skald.core.exceptions import NotInitializedError


def report() -> None:
    """Print engineering activity report."""
    if not is_initialized():
        raise NotInitializedError("Run `skald init` first.")
    ctx = build_context()
    render_report(ctx, Console())
