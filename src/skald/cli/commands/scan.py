"""skald scan commands."""

from __future__ import annotations

import typer
from rich.console import Console

from skald.application.scan_git import scan_git_use_case
from skald.application.scan_repository import scan_repository_use_case
from skald.core.config import is_initialized
from skald.core.container import build_context
from skald.core.exceptions import NotInitializedError
from skald.providers.git.github import GitHubProvider

app = typer.Typer(help="Scan repositories and git history.")
console = Console()


def _require_init() -> None:
    if not is_initialized():
        raise NotInitializedError("Run `skald init` first.")


@app.command("repo")
def scan_repo(
    path: str = typer.Argument(..., help="Path to git repository"),
) -> None:
    """Scan repository structure and metadata."""
    _require_init()
    ctx = build_context()
    repo_id = scan_repository_use_case(ctx, path)
    console.print(f"[green]Repository scanned[/green] id={repo_id}")


@app.command("git")
def scan_git(
    path: str = typer.Argument(..., help="Path to git repository"),
    limit: int | None = typer.Option(None, "--limit", help="Max commits to scan"),
    since_sha: str | None = typer.Option(None, "--since-sha", help="Scan commits after SHA"),
) -> None:
    """Scan git commit history."""
    _require_init()
    ctx = build_context()
    count = scan_git_use_case(ctx, path, limit=limit, since_sha=since_sha)
    console.print(f"[green]Stored {count} commit(s)[/green]")


@app.command("github")
def scan_github(
    user: str = typer.Option(..., "--user", help="GitHub username"),
) -> None:
    """Discover public GitHub repositories (metadata listing)."""
    _require_init()
    ctx = build_context()
    provider = GitHubProvider(token_env=ctx.config.github.token_env)
    repos = provider.list_public_repositories(user)
    console.print(f"[green]Found {len(repos)} repositories for {user}[/green]")
    for repo in repos[:25]:
        console.print(f"  - {repo.get('full_name')} ({repo.get('language') or 'unknown'})")
    if len(repos) > 25:
        console.print(f"  ... and {len(repos) - 25} more")
