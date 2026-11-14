"""Feature discovery orchestration."""

from __future__ import annotations

import uuid
from datetime import datetime

from skald.analysis.commit_grouping import DeterministicGroupingStrategy
from skald.core.config import AnalysisSettings
from skald.domain.grouping import CommitGroup, dominant_title
from skald.schemas.commit import CommitMetadata
from skald.schemas.feature import FeatureMetadata, ImplementationStep, SourceRef
from skald.schemas.repository import RepositoryMetadata

FEATURE_NS = uuid.UUID("a3f2c8e1-4b5d-4e6f-9a0b-1c2d3e4f5a6b")


def discover_features(
    repository: RepositoryMetadata | None,
    commits: list[CommitMetadata],
    settings: AnalysisSettings,
) -> list[FeatureMetadata]:
    strategy = DeterministicGroupingStrategy()
    groups = strategy.group(commits, settings)
    features: list[FeatureMetadata] = []
    tech = list(repository.frameworks) if repository else []
    if repository and repository.primary_language:
        tech.append(repository.primary_language)

    for group in groups:
        features.append(_group_to_feature(group, repository, tech, settings))
    return features


def _group_to_feature(
    group: CommitGroup,
    repository: RepositoryMetadata | None,
    technologies: list[str],
    settings: AnalysisSettings,
) -> FeatureMetadata:
    shas = [c.sha for c in group.commits]
    files = sorted({cf.path for c in group.commits for cf in c.changed_files})
    title = dominant_title(group.commits)
    summary = _build_summary(group.commits)
    if group.confidence >= settings.minimum_group_confidence:
        status = "discovered"
    else:
        status = "needs_review"
    steps = [
        {
            "order": i + 1,
            "description": c.message.splitlines()[0][:300],
            "sources": [SourceRef(commit_sha=c.sha, kind="observed")],
        }
        for i, c in enumerate(group.commits)
    ]
    repo_key = repository.id if repository else "global"
    stable_id = str(uuid.uuid5(FEATURE_NS, f"{repo_key}:{':'.join(sorted(shas))}"))
    return FeatureMetadata(
        id=stable_id,
        title=title,
        summary=summary,
        category="engineering",
        technologies=sorted(set(technologies)),
        technical_context=(
            repository.documentation.summaries[0]
            if repository and repository.documentation.summaries
            else None
        ),
        related_commits=shas,
        related_files=files,
        confidence=round(group.confidence, 3),
        status=status,  # type: ignore[arg-type]
        repository_id=(
            repository.id
            if repository
            else (group.commits[0].repository_id if group.commits else None)
        ),
        implementation_steps=[ImplementationStep.model_validate(s) for s in steps],
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
    )


def _build_summary(commits: list[CommitMetadata]) -> str:
    if not commits:
        return "No commits in group."
    lines = [c.message.splitlines()[0] for c in commits[:5]]
    return "; ".join(ln for ln in lines if ln)
