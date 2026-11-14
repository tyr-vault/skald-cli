"""Feature query use cases."""

from __future__ import annotations

from pathlib import Path

from skald.core.container import AppContext
from skald.core.exceptions import NotFoundError
from skald.schemas.feature import FeatureMetadata
from skald.schemas.serialization import write_yaml


def list_features(ctx: AppContext) -> list[FeatureMetadata]:
    return ctx.knowledge.list_features()


def get_feature(ctx: AppContext, feature_id: str) -> FeatureMetadata:
    feature = ctx.knowledge.get_feature(feature_id)
    if feature is None:
        raise NotFoundError(f"Feature not found: {feature_id}")
    return feature


def export_feature(ctx: AppContext, feature_id: str, fmt: str) -> Path:
    feature = get_feature(ctx, feature_id)
    if fmt != "yaml":
        raise ValueError(f"Unsupported export format: {fmt}")
    out = Path(ctx.config.workspace.path) / "features" / f"{feature_id}.yaml"
    write_yaml(out, feature)
    return out
