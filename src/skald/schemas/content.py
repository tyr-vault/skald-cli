"""Content metadata schemas."""

from __future__ import annotations

from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field


class ContentMetadata(BaseModel):
    id: str
    feature_id: str
    format: Literal["article", "learning-note", "linkedin"]
    title: str
    language: str = "en"
    output_path: str
    status: Literal["draft", "final"] = "draft"
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
