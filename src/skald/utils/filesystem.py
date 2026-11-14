"""Filesystem helpers."""

from __future__ import annotations

from pathlib import Path


def ensure_dir(path: Path) -> Path:
    path.mkdir(parents=True, exist_ok=True)
    return path


def workspace_artifacts(workspace: Path, repository_id: str, *parts: str) -> Path:
    base = workspace / "artifacts" / repository_id
    for part in parts:
        base = base / part
    return ensure_dir(base.parent) if parts else ensure_dir(base)
