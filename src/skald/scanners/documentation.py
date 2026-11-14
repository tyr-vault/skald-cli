"""Documentation scanner."""

from __future__ import annotations

from pathlib import Path

from skald.schemas.repository import DocumentationRefs
from skald.utils.sanitize import is_sensitive_path

DOC_CANDIDATES = ("README.md", "README", "readme.md", "CONTRIBUTING.md", "CHANGELOG.md")


def scan_documentation(repo_path: Path) -> DocumentationRefs:
    files: list[str] = []
    summaries: list[str] = []
    for name in DOC_CANDIDATES:
        candidate = repo_path / name
        if candidate.is_file() and not is_sensitive_path(name):
            files.append(name)
            text = candidate.read_text(encoding="utf-8", errors="ignore")
            first_para = _first_paragraph(text)
            if first_para:
                summaries.append(first_para[:500])
    docs_dir = repo_path / "docs"
    if docs_dir.is_dir():
        for md in sorted(docs_dir.rglob("*.md"))[:20]:
            rel = str(md.relative_to(repo_path))
            if is_sensitive_path(rel):
                continue
            files.append(rel)
    return DocumentationRefs(files=files, summaries=summaries)


def _first_paragraph(text: str) -> str:
    lines = [ln.strip() for ln in text.splitlines() if ln.strip()]
    if not lines:
        return ""
    buf: list[str] = []
    for ln in lines:
        if ln.startswith("#"):
            continue
        if not buf and ln.startswith(("#", "[")):
            continue
        buf.append(ln)
        if len(buf) >= 3:
            break
    return " ".join(buf)
