"""CLI entry point."""

from __future__ import annotations

import typer

from skald.cli.app import app
from skald.core.exceptions import NotInitializedError, SkaldError
from skald.core.logging import setup_logging


def main() -> None:
    setup_logging()
    try:
        app()
    except NotInitializedError as exc:
        typer.secho(str(exc), fg=typer.colors.RED, err=True)
        raise typer.Exit(code=1) from exc
    except SkaldError as exc:
        typer.secho(str(exc), fg=typer.colors.RED, err=True)
        raise typer.Exit(code=1) from exc


if __name__ == "__main__":
    main()
