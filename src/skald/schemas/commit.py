"""Commit metadata schemas."""

from __future__ import annotations

from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field


class ChangedFile(BaseModel):
    path: str
    change_type: Literal["add", "modify", "delete", "rename", "unknown"] = "unknown"
    additions: int = 0
    deletions: int = 0


class CommitMetadata(BaseModel):
    sha: str
    repository_id: str
    author: str
    author_email: str
    authored_at: datetime
    committed_at: datetime
    message: str
    changed_files: list[ChangedFile] = Field(default_factory=list)
    additions: int = 0
    deletions: int = 0
    diff_reference: str | None = None
    parent_shas: list[str] = Field(default_factory=list)
    is_merge: bool = False
