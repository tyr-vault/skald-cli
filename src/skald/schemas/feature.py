"""Feature metadata schemas."""

from __future__ import annotations

from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field


class SourceRef(BaseModel):
    commit_sha: str | None = None
    file_path: str | None = None
    kind: Literal["observed", "inferred"] = "observed"
    note: str | None = None


class ImplementationStep(BaseModel):
    order: int
    description: str
    sources: list[SourceRef] = Field(default_factory=list)


class ArchitecturalDecision(BaseModel):
    decision: str
    rationale: str | None = None
    sources: list[SourceRef] = Field(default_factory=list)


class Tradeoff(BaseModel):
    topic: str
    choice: str
    tradeoff: str | None = None
    sources: list[SourceRef] = Field(default_factory=list)


class TechnicalConcept(BaseModel):
    name: str
    description: str | None = None
    sources: list[SourceRef] = Field(default_factory=list)


class LearningOpportunity(BaseModel):
    topic: str
    description: str
    sources: list[SourceRef] = Field(default_factory=list)


class FeatureMetadata(BaseModel):
    id: str
    title: str
    summary: str
    category: str | None = None
    subcategory: str | None = None
    technologies: list[str] = Field(default_factory=list)
    technical_context: str | None = None
    problem: str | None = None
    motivation: str | None = None
    solution: str | None = None
    implementation_steps: list[ImplementationStep] = Field(default_factory=list)
    architectural_decisions: list[ArchitecturalDecision] = Field(default_factory=list)
    tradeoffs: list[Tradeoff] = Field(default_factory=list)
    technical_concepts: list[TechnicalConcept] = Field(default_factory=list)
    learning_opportunities: list[LearningOpportunity] = Field(default_factory=list)
    related_commits: list[str] = Field(default_factory=list)
    related_files: list[str] = Field(default_factory=list)
    confidence: float = 0.0
    status: Literal["discovered", "needs_review", "documented"] = "discovered"
    repository_id: str | None = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
