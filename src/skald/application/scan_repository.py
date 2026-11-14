"""Scan repository metadata."""

from __future__ import annotations

from pathlib import Path

from skald.core.container import AppContext
from skald.scanners.repository import scan_repository
from skald.storage.repositories import new_repository_id


def scan_repository_use_case(ctx: AppContext, repo_path: str) -> str:
    path = Path(repo_path).resolve()
    existing = ctx.knowledge.get_repository_by_path(str(path))
    repo_id = existing.id if existing else new_repository_id()
    meta = scan_repository(path, repository_id=repo_id)
    ctx.knowledge.upsert_repository(meta)
    return meta.id
