"""Commit normalization for analysis."""

from __future__ import annotations

from skald.domain.grouping import NormalizedCommit, normalize_commits
from skald.schemas.commit import CommitMetadata

__all__ = ["NormalizedCommit", "normalize_commits", "normalize_commit_list"]


def normalize_commit_list(commits: list[CommitMetadata]) -> list[NormalizedCommit]:
    return normalize_commits(commits)
