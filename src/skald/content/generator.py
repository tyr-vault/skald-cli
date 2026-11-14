"""Jinja-based content generation."""

from __future__ import annotations

from pathlib import Path

import jinja2

from skald.core.config import SkaldConfig
from skald.schemas.feature import FeatureMetadata
from skald.utils.filesystem import ensure_dir

TEMPLATE_DIR = Path(__file__).parent / "templates"

FORMAT_TEMPLATE = {
    "article": "article.md.j2",
    "learning-note": "learning_note.md.j2",
    "linkedin": "linkedin.md.j2",
}


def generate_draft(config: SkaldConfig, feature: FeatureMetadata, fmt: str) -> tuple[Path, str]:
    if fmt not in FORMAT_TEMPLATE:
        raise ValueError(f"Unknown format: {fmt}")
    env = jinja2.Environment(
        loader=jinja2.FileSystemLoader(str(TEMPLATE_DIR)),
        autoescape=False,
        trim_blocks=True,
        lstrip_blocks=True,
    )
    template = env.get_template(FORMAT_TEMPLATE[fmt])
    commits_detail = [{"sha": sha, "short": sha[:8]} for sha in feature.related_commits]
    body = template.render(
        feature=feature,
        commits=commits_detail,
        files=feature.related_files,
        has_evidence=bool(feature.related_commits or feature.related_files),
    )
    title = feature.title
    slug = _slugify(title)
    out_dir = ensure_dir(config.content.output_directory)
    path = out_dir / f"{slug}-{fmt}.md"
    path.write_text(body, encoding="utf-8")
    return path, title


def _slugify(value: str) -> str:
    keep = "".join(c if c.isalnum() or c in "-_" else "-" for c in value.lower())
    while "--" in keep:
        keep = keep.replace("--", "-")
    return keep.strip("-")[:60] or "draft"
