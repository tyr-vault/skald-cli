"""Repository metadata schemas."""

from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field


class LanguageStat(BaseModel):
    language: str
    file_count: int = 0
    byte_estimate: int = 0


class DependencySet(BaseModel):
    ecosystem: str
    dependencies: list[str] = Field(default_factory=list)


class ArchitectureHints(BaseModel):
    patterns: list[str] = Field(default_factory=list)
    layers: list[str] = Field(default_factory=list)
    evidence: list[str] = Field(default_factory=list)


class DocumentationRefs(BaseModel):
    files: list[str] = Field(default_factory=list)
    summaries: list[str] = Field(default_factory=list)


class InfrastructureHints(BaseModel):
    ci_systems: list[str] = Field(default_factory=list)
    config_files: list[str] = Field(default_factory=list)


class RepositoryMetadata(BaseModel):
    id: str
    name: str
    path: str
    remote_url: str | None = None
    primary_language: str | None = None
    languages: list[LanguageStat] = Field(default_factory=list)
    frameworks: list[str] = Field(default_factory=list)
    dependencies: list[DependencySet] = Field(default_factory=list)
    architecture: ArchitectureHints = Field(default_factory=ArchitectureHints)
    documentation: DocumentationRefs = Field(default_factory=DocumentationRefs)
    infrastructure: InfrastructureHints = Field(default_factory=InfrastructureHints)
    last_analyzed_commit: str | None = None
    analyzed_at: datetime | None = None
