"""Scan git history."""

from __future__ import annotations

from pathlib import Path

from skald.core.container import AppContext
from skald.core.exceptions import NotFoundError
from skald.providers.git.local import LocalGitProvider


def scan_git_use_case(
    ctx: AppContext,
    repo_path: str,
    *,
    limit: int | None = None,
    since_sha: str | None = None,
) -> int:
    path = Path(repo_path).resolve()
    meta = ctx.knowledge.get_repository_by_path(str(path))
    if meta is None:
        from skald.application.scan_repository import scan_repository_use_case

        repo_id = scan_repository_use_case(ctx, str(path))
        meta = ctx.knowledge.get_repository_by_path(str(path))
        if meta is None:
            raise NotFoundError("Repository metadata missing after scan")
        repo_id = meta.id
    else:
        repo_id = meta.id

    if since_sha is None:
        since_sha = ctx.knowledge.get_scan_state(repo_id)

    provider = LocalGitProvider()
    commits = provider.iter_commits(
        str(path),
        repository_id=repo_id,
        limit=limit or ctx.config.analysis.default_history_limit,
        since_sha=since_sha,
        workspace=ctx.workspace,
        max_diff_size=ctx.config.analysis.max_diff_size,
    )
    for commit in commits:
        ctx.knowledge.upsert_commit(commit)
    if commits:
        ctx.knowledge.set_scan_state(repo_id, commits[0].sha)
    return len(commits)
