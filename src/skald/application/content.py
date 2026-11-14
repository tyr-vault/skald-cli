"""Content draft generation."""

from __future__ import annotations

from datetime import datetime
from uuid import uuid4

from skald.application.features import get_feature
from skald.content.generator import generate_draft
from skald.core.container import AppContext
from skald.schemas.content import ContentMetadata


def draft_content(ctx: AppContext, feature_id: str, fmt: str) -> ContentMetadata:
    feature = get_feature(ctx, feature_id)
    path, title = generate_draft(ctx.config, feature, fmt)
    meta = ContentMetadata(
        id=str(uuid4()),
        feature_id=feature_id,
        format=fmt,  # type: ignore[arg-type]
        title=title,
        language=ctx.config.content.default_language,
        output_path=str(path),
        status="draft",
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
    )
    ctx.knowledge.save_content(meta)
    return meta
