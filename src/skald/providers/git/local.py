"""Local GitPython provider."""

from __future__ import annotations

from pathlib import Path

from git import Repo
from git.exc import InvalidGitRepositoryError

from skald.core.exceptions import RepositoryError
from skald.providers.git.base import GitProvider
from skald.scanners.git import extract_commits
from skald.schemas.commit import CommitMetadata


class LocalGitProvider(GitProvider):
    def iter_commits(
        self,
        repository_path: str,
        *,
        repository_id: str,
        limit: int,
        since_sha: str | None,
        workspace: str,
        max_diff_size: int,
    ) -> list[CommitMetadata]:
        path = Path(repository_path).resolve()
        if not path.is_dir():
            raise RepositoryError(f"Not a directory: {path}")
        try:
            Repo(path)
        except InvalidGitRepositoryError as exc:
            raise RepositoryError(f"Not a git repository: {path}") from exc
        return extract_commits(
            path,
            repository_id=repository_id,
            limit=limit,
            since_sha=since_sha,
            workspace=Path(workspace),
            max_diff_size=max_diff_size,
        )
