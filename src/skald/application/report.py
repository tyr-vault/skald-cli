"""Engineering activity report."""

from __future__ import annotations

from collections import Counter

from rich.console import Console
from rich.table import Table

from skald.core.container import AppContext


def render_report(ctx: AppContext, console: Console | None = None) -> None:
    console = console or Console()
    repos = ctx.knowledge.list_repositories()
    features = ctx.knowledge.list_features()
    commits_count = ctx.knowledge.count_commits()

    tech: Counter[str] = Counter()
    for repo in repos:
        if repo.primary_language:
            tech[repo.primary_language] += 1
        tech.update(repo.frameworks)

    table = Table(title="Skald Engineering Activity Report")
    table.add_column("Metric")
    table.add_column("Value")
    table.add_row("Repositories analyzed", str(len(repos)))
    table.add_row("Commits analyzed", str(commits_count))
    table.add_row("Features discovered", str(len(features)))
    table.add_row("Main technologies", ", ".join(t for t, _ in tech.most_common(8)) or "—")
    table.add_row(
        "Content opportunities",
        str(
            len(
                [
                    f
                    for f in features
                    if f.confidence >= ctx.config.analysis.minimum_group_confidence
                ]
            )
        ),
    )
    console.print(table)

    if features:
        topics = Table(title="Technical topics (features)")
        topics.add_column("ID")
        topics.add_column("Title")
        topics.add_column("Confidence")
        for f in features[:15]:
            topics.add_row(f.id[:8], f.title[:60], f"{f.confidence:.2f}")
        console.print(topics)
