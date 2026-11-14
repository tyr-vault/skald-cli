"""Run analysis pipeline."""

from __future__ import annotations

from skald.analysis.feature_discovery import discover_features
from skald.core.container import AppContext


def analyze_use_case(ctx: AppContext, repository_id: str | None = None) -> int:
    repos = ctx.knowledge.list_repositories()
    if repository_id:
        repos = [r for r in repos if r.id == repository_id]
    total = 0
    for repo in repos:
        commits = ctx.knowledge.list_commits(repo.id)
        features = discover_features(repo, commits, ctx.config.analysis)
        for feature in features:
            related = [c for c in commits if c.sha in feature.related_commits]
            enriched = ctx.knowledge_extractor.enrich(feature, related, repo)
            ctx.knowledge.upsert_feature(enriched)
            total += 1
    return total
