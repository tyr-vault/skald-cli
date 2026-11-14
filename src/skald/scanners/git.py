"""Git history scanner."""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path

from git import Repo

from skald.schemas.commit import ChangedFile, CommitMetadata
from skald.utils.filesystem import ensure_dir
from skald.utils.sanitize import is_sensitive_path


def _change_type(name: str, change_type_char: str) -> str:
    if change_type_char == "A":
        return "add"
    if change_type_char == "D":
        return "delete"
    if change_type_char == "M":
        return "modify"
    if change_type_char == "R":
        return "rename"
    return "unknown"


def extract_commits(
    repo_path: Path,
    *,
    repository_id: str,
    limit: int,
    since_sha: str | None,
    workspace: Path,
    max_diff_size: int,
) -> list[CommitMetadata]:
    repo = Repo(repo_path)
    commits: list[CommitMetadata] = []
    diff_dir = ensure_dir(workspace / "artifacts" / repository_id / "diffs")

    if since_sha:
        commit_iter = repo.iter_commits(f"{since_sha}..HEAD", max_count=limit)
    else:
        commit_iter = repo.iter_commits(max_count=limit)

    for commit in commit_iter:
        stats = commit.stats
        changed_files: list[ChangedFile] = []
        for path, stat in stats.files.items():
            path_str = str(path)
            if is_sensitive_path(path_str):
                continue
            changed_files.append(
                ChangedFile(
                    path=path_str,
                    change_type="modify",
                    additions=stat.get("insertions", 0),
                    deletions=stat.get("deletions", 0),
                )
            )
        diff_ref: str | None = None
        try:
            diff_text = repo.git.diff(commit.hexsha + "^", commit.hexsha, unified=3)
            if diff_text and not _diff_contains_sensitive(diff_text):
                if len(diff_text) > max_diff_size:
                    diff_text = diff_text[:max_diff_size] + "\n\n[diff truncated by skald]\n"
                diff_file = diff_dir / f"{commit.hexsha}.patch"
                diff_file.write_text(diff_text, encoding="utf-8")
                diff_ref = str(diff_file)
        except Exception:
            diff_ref = None

        authored = datetime.fromtimestamp(commit.authored_date, tz=timezone.utc).replace(
            tzinfo=None
        )
        committed = datetime.fromtimestamp(commit.committed_date, tz=timezone.utc).replace(
            tzinfo=None
        )
        commits.append(
            CommitMetadata(
                sha=commit.hexsha,
                repository_id=repository_id,
                author=commit.author.name or "unknown",
                author_email=commit.author.email or "",
                authored_at=authored,
                committed_at=committed,
                message=_commit_message(commit.message),
                changed_files=changed_files,
                additions=stats.total["insertions"],
                deletions=stats.total["deletions"],
                diff_reference=diff_ref,
                parent_shas=[p.hexsha for p in commit.parents],
                is_merge=len(commit.parents) > 1,
            )
        )
    return commits


def _commit_message(message: str | bytes | None) -> str:
    if message is None:
        return ""
    if isinstance(message, bytes):
        return message.decode("utf-8", errors="replace")
    return message


def _diff_contains_sensitive(diff_text: str) -> bool:
    for line in diff_text.splitlines():
        if line.startswith("+++") or line.startswith("---"):
            path = line[4:].strip().lstrip("ab/")
            if is_sensitive_path(path):
                return True
    return False
