"""Git provider base types."""

from __future__ import annotations

from abc import ABC, abstractmethod

from skald.schemas.commit import CommitMetadata


class GitProvider(ABC):
    @abstractmethod
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
        raise NotImplementedError
