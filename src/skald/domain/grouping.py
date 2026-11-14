"""Pure feature grouping domain logic."""

from __future__ import annotations

import re
from dataclasses import dataclass
from datetime import datetime

from skald.core.config import AnalysisSettings
from skald.schemas.commit import CommitMetadata

STOP_WORDS = frozenset(
    {
        "a",
        "an",
        "the",
        "and",
        "or",
        "for",
        "to",
        "in",
        "of",
        "with",
        "fix",
        "feat",
        "chore",
        "docs",
        "test",
        "merge",
        "branch",
    }
)

TECH_KEYWORDS = frozenset(
    {
        "api",
        "auth",
        "database",
        "sql",
        "redis",
        "docker",
        "kubernetes",
        "pytest",
        "react",
        "python",
        "typescript",
        "graphql",
        "rest",
        "cli",
        "config",
        "migration",
    }
)


@dataclass(frozen=True)
class NormalizedCommit:
    commit: CommitMetadata
    tokens: frozenset[str]
    directories: frozenset[str]
    concepts: frozenset[str]
    paths: frozenset[str]


class UnionFind:
    def __init__(self, n: int) -> None:
        self.parent = list(range(n))

    def find(self, x: int) -> int:
        while self.parent[x] != x:
            self.parent[x] = self.parent[self.parent[x]]
            x = self.parent[x]
        return x

    def union(self, a: int, b: int) -> None:
        ra, rb = self.find(a), self.find(b)
        if ra != rb:
            self.parent[rb] = ra


def tokenize_message(message: str) -> frozenset[str]:
    line = message.splitlines()[0].lower()
    line = re.sub(r"^(feat|fix|chore|docs|test|refactor|ci)(\([^)]+\))?:\s*", "", line)
    tokens = {t for t in re.findall(r"[a-z0-9]+", line) if t not in STOP_WORDS and len(t) > 2}
    return frozenset(tokens)


def directories_from_paths(paths: frozenset[str]) -> frozenset[str]:
    dirs: set[str] = set()
    for p in paths:
        parts = p.replace("\\", "/").split("/")
        if len(parts) >= 2:
            dirs.add("/".join(parts[:2]))
        elif parts:
            dirs.add(parts[0])
    return frozenset(dirs)


def concepts_from_commit(message: str, paths: frozenset[str]) -> frozenset[str]:
    text = message.lower()
    found = {kw for kw in TECH_KEYWORDS if kw in text}
    for p in paths:
        ext = p.rsplit(".", 1)[-1].lower() if "." in p else ""
        ext_map = {"py": "python", "ts": "typescript", "tsx": "typescript", "js": "javascript"}
        if ext in ext_map:
            found.add(ext_map[ext])
    return frozenset(found)


def jaccard(a: frozenset[str], b: frozenset[str]) -> float:
    if not a and not b:
        return 0.0
    inter = len(a & b)
    union = len(a | b)
    return inter / union if union else 0.0


def temporal_score(a: datetime, b: datetime, window_hours: int) -> float:
    delta_h = abs((a - b).total_seconds()) / 3600.0
    if delta_h > window_hours:
        return 0.0
    return max(0.0, 1.0 - delta_h / window_hours)


def affinity(na: NormalizedCommit, nb: NormalizedCommit, settings: AnalysisSettings) -> float:
    msg = jaccard(na.tokens, nb.tokens)
    temporal = temporal_score(
        na.commit.authored_at, nb.commit.authored_at, settings.grouping_window_hours
    )
    files = jaccard(na.paths, nb.paths)
    dirs = jaccard(na.directories, nb.directories)
    concepts = jaccard(na.concepts, nb.concepts)

    score = (
        settings.message_weight * msg
        + settings.temporal_weight * temporal
        + settings.file_weight * files
        + settings.directory_weight * dirs
        + settings.concept_weight * concepts
    )
    # Time alone cannot push over threshold
    non_temporal = (
        settings.message_weight * msg
        + settings.file_weight * files
        + settings.directory_weight * dirs
        + settings.concept_weight * concepts
    )
    if non_temporal < 0.15 and temporal > 0:
        score = min(score, settings.minimum_group_confidence - 0.01)
    if files >= 0.4 and dirs >= 0.5:
        score = max(score, settings.minimum_group_confidence)
    return score


def normalize_commits(commits: list[CommitMetadata]) -> list[NormalizedCommit]:
    result: list[NormalizedCommit] = []
    for c in commits:
        paths = frozenset(cf.path for cf in c.changed_files)
        result.append(
            NormalizedCommit(
                commit=c,
                tokens=tokenize_message(c.message),
                directories=directories_from_paths(paths),
                concepts=concepts_from_commit(c.message, paths),
                paths=paths,
            )
        )
    return result


@dataclass
class CommitGroup:
    commits: list[CommitMetadata]
    confidence: float


def group_commits(
    commits: list[CommitMetadata],
    settings: AnalysisSettings,
) -> list[CommitGroup]:
    if not commits:
        return []
    normalized = normalize_commits(commits)
    n = len(normalized)
    uf = UnionFind(n)
    edge_scores: list[tuple[int, int, float]] = []

    for i in range(n):
        for j in range(i + 1, n):
            s = affinity(normalized[i], normalized[j], settings)
            if s >= settings.minimum_group_confidence:
                uf.union(i, j)
                edge_scores.append((i, j, s))

    buckets: dict[int, list[int]] = {}
    for idx in range(n):
        root = uf.find(idx)
        buckets.setdefault(root, []).append(idx)

    groups: list[CommitGroup] = []
    for indices in buckets.values():
        group_commits_list = [normalized[i].commit for i in indices]
        if len(indices) == 1:
            groups.append(CommitGroup(commits=group_commits_list, confidence=0.55))
            continue
        scores = [
            edge_scores[k][2]
            for k, (i, j, _) in enumerate(edge_scores)
            if uf.find(i) == uf.find(indices[0]) or uf.find(j) == uf.find(indices[0])
        ]
        conf = float(sum(scores) / len(scores)) if scores else settings.minimum_group_confidence
        conf = max(settings.minimum_group_confidence, min(1.0, conf))
        groups.append(CommitGroup(commits=group_commits_list, confidence=conf))
    return groups


def dominant_title(commits: list[CommitMetadata]) -> str:
    if not commits:
        return "Undocumented feature"
    first = commits[0].message.splitlines()[0].strip()
    return first[:200] if first else "Engineering change"
