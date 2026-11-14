"""Domain port protocols."""

from __future__ import annotations

from typing import Protocol

from skald.schemas.commit import CommitMetadata
from skald.schemas.repository import RepositoryMetadata


class CommitReader(Protocol):
    def iter_commits(
        self,
        repo_path: str,
        *,
        limit: int,
        since_sha: str | None,
    ) -> list[CommitMetadata]: ...


class RepositoryInspector(Protocol):
    def inspect(self, repo_path: str) -> RepositoryMetadata: ...


class LLMCompleter(Protocol):
    def complete_json(self, prompt: str, schema_hint: str) -> dict[str, object]: ...
