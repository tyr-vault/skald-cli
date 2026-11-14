from datetime import datetime, timedelta

from skald.core.config import AnalysisSettings
from skald.domain.grouping import group_commits
from skald.schemas.commit import ChangedFile, CommitMetadata


def _commit(sha: str, msg: str, paths: list[str], offset_hours: int = 0) -> CommitMetadata:
    base = datetime(2025, 1, 1, 12, 0, 0)
    return CommitMetadata(
        sha=sha,
        repository_id="r1",
        author="a",
        author_email="a@b.c",
        authored_at=base + timedelta(hours=offset_hours),
        committed_at=base + timedelta(hours=offset_hours),
        message=msg,
        changed_files=[ChangedFile(path=p) for p in paths],
    )


def test_groups_related_commits_by_files_and_messages() -> None:
    commits = [
        _commit("a" * 40, "feat: add user auth module", ["src/auth/login.py"]),
        _commit(
            "b" * 40,
            "feat: wire auth middleware",
            ["src/auth/login.py", "src/auth/middleware.py"],
            2,
        ),
    ]
    groups = group_commits(commits, AnalysisSettings())
    assert len(groups) == 1
    assert len(groups[0].commits) == 2
    assert groups[0].confidence >= 0.65


def test_does_not_group_unrelated_commits_by_time_alone() -> None:
    commits = [
        _commit("c" * 40, "docs: update readme", ["README.md"]),
        _commit("d" * 40, "chore: unrelated ci tweak", [".github/workflows/ci.yml"], 1),
    ]
    groups = group_commits(commits, AnalysisSettings())
    assert len(groups) == 2
