"""SQLAlchemy ORM models."""

from __future__ import annotations

from datetime import datetime

from sqlalchemy import Boolean, DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class RepositoryRow(Base):
    __tablename__ = "repositories"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    name: Mapped[str] = mapped_column(String(255))
    path: Mapped[str] = mapped_column(Text)
    remote_url: Mapped[str | None] = mapped_column(Text, nullable=True)
    primary_language: Mapped[str | None] = mapped_column(String(64), nullable=True)
    payload_json: Mapped[str] = mapped_column(Text)
    last_analyzed_commit: Mapped[str | None] = mapped_column(String(40), nullable=True)
    analyzed_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)

    commits: Mapped[list[CommitRow]] = relationship(back_populates="repository")
    scan_state: Mapped[ScanStateRow | None] = relationship(
        back_populates="repository", uselist=False
    )


class CommitRow(Base):
    __tablename__ = "commits"

    sha: Mapped[str] = mapped_column(String(40), primary_key=True)
    repository_id: Mapped[str] = mapped_column(ForeignKey("repositories.id"), primary_key=True)
    author: Mapped[str] = mapped_column(String(255))
    author_email: Mapped[str] = mapped_column(String(255))
    authored_at: Mapped[datetime] = mapped_column(DateTime)
    committed_at: Mapped[datetime] = mapped_column(DateTime)
    message: Mapped[str] = mapped_column(Text)
    additions: Mapped[int] = mapped_column(Integer, default=0)
    deletions: Mapped[int] = mapped_column(Integer, default=0)
    diff_reference: Mapped[str | None] = mapped_column(Text, nullable=True)
    parent_shas: Mapped[str] = mapped_column(Text, default="")
    is_merge: Mapped[bool] = mapped_column(Boolean, default=False)
    payload_json: Mapped[str] = mapped_column(Text, default="{}")

    repository: Mapped[RepositoryRow] = relationship(back_populates="commits")


class CommitFileRow(Base):
    __tablename__ = "commit_files"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    repository_id: Mapped[str] = mapped_column(String(36))
    commit_sha: Mapped[str] = mapped_column(String(40))
    path: Mapped[str] = mapped_column(Text)
    change_type: Mapped[str] = mapped_column(String(16))
    additions: Mapped[int] = mapped_column(Integer, default=0)
    deletions: Mapped[int] = mapped_column(Integer, default=0)


class FeatureRow(Base):
    __tablename__ = "features"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    repository_id: Mapped[str | None] = mapped_column(String(36), nullable=True)
    title: Mapped[str] = mapped_column(String(512))
    confidence: Mapped[float] = mapped_column(Float, default=0.0)
    status: Mapped[str] = mapped_column(String(32))
    payload_json: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime)
    updated_at: Mapped[datetime] = mapped_column(DateTime)


class FeatureCommitRow(Base):
    __tablename__ = "feature_commits"

    feature_id: Mapped[str] = mapped_column(ForeignKey("features.id"), primary_key=True)
    commit_sha: Mapped[str] = mapped_column(String(40), primary_key=True)
    repository_id: Mapped[str] = mapped_column(String(36), primary_key=True)


class FeatureFileRow(Base):
    __tablename__ = "feature_files"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    feature_id: Mapped[str] = mapped_column(ForeignKey("features.id"))
    path: Mapped[str] = mapped_column(Text)


class ContentRow(Base):
    __tablename__ = "content_artifacts"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    feature_id: Mapped[str] = mapped_column(ForeignKey("features.id"))
    format: Mapped[str] = mapped_column(String(32))
    title: Mapped[str] = mapped_column(String(512))
    language: Mapped[str] = mapped_column(String(8))
    output_path: Mapped[str] = mapped_column(Text)
    status: Mapped[str] = mapped_column(String(16))
    created_at: Mapped[datetime] = mapped_column(DateTime)
    updated_at: Mapped[datetime] = mapped_column(DateTime)


class ScanStateRow(Base):
    __tablename__ = "scan_state"

    repository_id: Mapped[str] = mapped_column(ForeignKey("repositories.id"), primary_key=True)
    last_scanned_sha: Mapped[str | None] = mapped_column(String(40), nullable=True)
    last_scanned_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)

    repository: Mapped[RepositoryRow] = relationship(back_populates="scan_state")
