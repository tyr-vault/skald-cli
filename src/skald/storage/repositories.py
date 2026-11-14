"""Persistence repositories (repository pattern)."""

from __future__ import annotations

import json
from datetime import datetime
from uuid import uuid4

from sqlalchemy import delete, select
from sqlalchemy.orm import Session, sessionmaker

from skald.schemas.commit import CommitMetadata
from skald.schemas.content import ContentMetadata
from skald.schemas.feature import FeatureMetadata
from skald.schemas.repository import RepositoryMetadata
from skald.storage.models import (
    CommitFileRow,
    CommitRow,
    ContentRow,
    FeatureCommitRow,
    FeatureFileRow,
    FeatureRow,
    RepositoryRow,
    ScanStateRow,
)


class KnowledgeRepository:
    def __init__(self, session_factory: sessionmaker[Session]) -> None:
        self._session_factory = session_factory

    def _session(self) -> Session:
        return self._session_factory()

    def upsert_repository(self, meta: RepositoryMetadata) -> None:
        with self._session() as session:
            row = session.get(RepositoryRow, meta.id)
            payload = meta.model_dump(mode="json")
            if row is None:
                row = RepositoryRow(
                    id=meta.id,
                    name=meta.name,
                    path=meta.path,
                    remote_url=meta.remote_url,
                    primary_language=meta.primary_language,
                    payload_json=json.dumps(payload),
                    last_analyzed_commit=meta.last_analyzed_commit,
                    analyzed_at=meta.analyzed_at,
                )
                session.add(row)
            else:
                row.name = meta.name
                row.path = meta.path
                row.remote_url = meta.remote_url
                row.primary_language = meta.primary_language
                row.payload_json = json.dumps(payload)
                row.last_analyzed_commit = meta.last_analyzed_commit
                row.analyzed_at = meta.analyzed_at
            session.commit()

    def get_repository_by_path(self, path: str) -> RepositoryMetadata | None:
        with self._session() as session:
            stmt = select(RepositoryRow).where(RepositoryRow.path == path)
            row = session.scalars(stmt).first()
            if row is None:
                return None
            data = json.loads(row.payload_json)
            return RepositoryMetadata.model_validate(data)

    def list_repositories(self) -> list[RepositoryMetadata]:
        with self._session() as session:
            rows = session.scalars(select(RepositoryRow)).all()
            return [RepositoryMetadata.model_validate(json.loads(r.payload_json)) for r in rows]

    def upsert_commit(self, meta: CommitMetadata) -> None:
        with self._session() as session:
            existing = session.get(CommitRow, (meta.sha, meta.repository_id))
            payload = meta.model_dump(mode="json")
            parent_str = ",".join(meta.parent_shas)
            if existing is None:
                row = CommitRow(
                    sha=meta.sha,
                    repository_id=meta.repository_id,
                    author=meta.author,
                    author_email=meta.author_email,
                    authored_at=meta.authored_at,
                    committed_at=meta.committed_at,
                    message=meta.message,
                    additions=meta.additions,
                    deletions=meta.deletions,
                    diff_reference=meta.diff_reference,
                    parent_shas=parent_str,
                    is_merge=meta.is_merge,
                    payload_json=json.dumps(payload),
                )
                session.add(row)
            else:
                existing.message = meta.message
                existing.additions = meta.additions
                existing.deletions = meta.deletions
                existing.diff_reference = meta.diff_reference
                existing.payload_json = json.dumps(payload)

            session.execute(
                delete(CommitFileRow).where(
                    CommitFileRow.repository_id == meta.repository_id,
                    CommitFileRow.commit_sha == meta.sha,
                )
            )
            for cf in meta.changed_files:
                session.add(
                    CommitFileRow(
                        repository_id=meta.repository_id,
                        commit_sha=meta.sha,
                        path=cf.path,
                        change_type=cf.change_type,
                        additions=cf.additions,
                        deletions=cf.deletions,
                    )
                )
            session.commit()

    def list_commits(self, repository_id: str | None = None) -> list[CommitMetadata]:
        with self._session() as session:
            stmt = select(CommitRow)
            if repository_id:
                stmt = stmt.where(CommitRow.repository_id == repository_id)
            rows = session.scalars(stmt).all()
            result: list[CommitMetadata] = []
            for row in rows:
                data = json.loads(row.payload_json)
                if not data.get("changed_files"):
                    files = session.scalars(
                        select(CommitFileRow).where(
                            CommitFileRow.repository_id == row.repository_id,
                            CommitFileRow.commit_sha == row.sha,
                        )
                    ).all()
                    data["changed_files"] = [
                        {
                            "path": f.path,
                            "change_type": f.change_type,
                            "additions": f.additions,
                            "deletions": f.deletions,
                        }
                        for f in files
                    ]
                result.append(CommitMetadata.model_validate(data))
            return result

    def count_commits(self) -> int:
        with self._session() as session:
            return len(session.scalars(select(CommitRow)).all())

    def get_scan_state(self, repository_id: str) -> str | None:
        with self._session() as session:
            row = session.get(ScanStateRow, repository_id)
            return row.last_scanned_sha if row else None

    def set_scan_state(self, repository_id: str, sha: str) -> None:
        with self._session() as session:
            row = session.get(ScanStateRow, repository_id)
            now = datetime.utcnow()
            if row is None:
                session.add(
                    ScanStateRow(
                        repository_id=repository_id,
                        last_scanned_sha=sha,
                        last_scanned_at=now,
                    )
                )
            else:
                row.last_scanned_sha = sha
                row.last_scanned_at = now
            session.commit()

    def upsert_feature(self, meta: FeatureMetadata) -> None:
        with self._session() as session:
            payload = meta.model_dump(mode="json")
            row = session.get(FeatureRow, meta.id)
            if row is None:
                row = FeatureRow(
                    id=meta.id,
                    repository_id=meta.repository_id,
                    title=meta.title,
                    confidence=meta.confidence,
                    status=meta.status,
                    payload_json=json.dumps(payload),
                    created_at=meta.created_at,
                    updated_at=meta.updated_at,
                )
                session.add(row)
            else:
                row.title = meta.title
                row.confidence = meta.confidence
                row.status = meta.status
                row.payload_json = json.dumps(payload)
                row.updated_at = meta.updated_at

            session.execute(delete(FeatureCommitRow).where(FeatureCommitRow.feature_id == meta.id))
            session.execute(delete(FeatureFileRow).where(FeatureFileRow.feature_id == meta.id))
            for sha in meta.related_commits:
                repo_id = meta.repository_id or ""
                session.add(
                    FeatureCommitRow(feature_id=meta.id, commit_sha=sha, repository_id=repo_id)
                )
            for path in meta.related_files:
                session.add(FeatureFileRow(feature_id=meta.id, path=path))
            session.commit()

    def list_features(self) -> list[FeatureMetadata]:
        with self._session() as session:
            rows = session.scalars(select(FeatureRow)).all()
            return [FeatureMetadata.model_validate(json.loads(r.payload_json)) for r in rows]

    def get_feature(self, feature_id: str) -> FeatureMetadata | None:
        with self._session() as session:
            row = session.get(FeatureRow, feature_id)
            if row is None:
                return None
            return FeatureMetadata.model_validate(json.loads(row.payload_json))

    def count_features(self) -> int:
        with self._session() as session:
            return len(session.scalars(select(FeatureRow)).all())

    def save_content(self, meta: ContentMetadata) -> None:
        with self._session() as session:
            row = session.get(ContentRow, meta.id)
            if row is None:
                session.add(
                    ContentRow(
                        id=meta.id,
                        feature_id=meta.feature_id,
                        format=meta.format,
                        title=meta.title,
                        language=meta.language,
                        output_path=meta.output_path,
                        status=meta.status,
                        created_at=meta.created_at,
                        updated_at=meta.updated_at,
                    )
                )
            else:
                row.output_path = meta.output_path
                row.status = meta.status
                row.updated_at = meta.updated_at
            session.commit()

    def list_content(self) -> list[ContentMetadata]:
        with self._session() as session:
            rows = session.scalars(select(ContentRow)).all()
            return [
                ContentMetadata(
                    id=r.id,
                    feature_id=r.feature_id,
                    format=r.format,  # type: ignore[arg-type]
                    title=r.title,
                    language=r.language,
                    output_path=r.output_path,
                    status=r.status,  # type: ignore[arg-type]
                    created_at=r.created_at,
                    updated_at=r.updated_at,
                )
                for r in rows
            ]


def new_repository_id() -> str:
    return str(uuid4())
