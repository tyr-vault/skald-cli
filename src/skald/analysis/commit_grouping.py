"""Grouping strategy protocol and deterministic implementation."""

from __future__ import annotations

from typing import Protocol

from skald.core.config import AnalysisSettings
from skald.domain.grouping import CommitGroup, group_commits
from skald.schemas.commit import CommitMetadata


class GroupingStrategy(Protocol):
    def group(
        self, commits: list[CommitMetadata], settings: AnalysisSettings
    ) -> list[CommitGroup]: ...


class DeterministicGroupingStrategy:
    def group(self, commits: list[CommitMetadata], settings: AnalysisSettings) -> list[CommitGroup]:
        return group_commits(commits, settings)


class SemanticGroupingStrategy:
    """Placeholder for future embedding/LLM grouping."""

    def group(self, commits: list[CommitMetadata], settings: AnalysisSettings) -> list[CommitGroup]:
        raise NotImplementedError("Semantic grouping is not available in the MVP")
