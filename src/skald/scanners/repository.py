"""Repository structure scanner."""

from __future__ import annotations

import json
import re
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from uuid import uuid4

from git import Repo
from git.exc import InvalidGitRepositoryError
from pathspec import PathSpec
from pathspec.patterns.gitwildmatch import GitWildMatchPattern

from skald.core.exceptions import RepositoryError
from skald.scanners.architecture import scan_architecture
from skald.scanners.documentation import scan_documentation
from skald.schemas.repository import (
    DependencySet,
    InfrastructureHints,
    LanguageStat,
    RepositoryMetadata,
)
from skald.utils.sanitize import is_sensitive_path

EXT_LANGUAGE = {
    ".py": "Python",
    ".js": "JavaScript",
    ".ts": "TypeScript",
    ".tsx": "TypeScript",
    ".go": "Go",
    ".rs": "Rust",
    ".java": "Java",
    ".rb": "Ruby",
    ".md": "Markdown",
    ".yaml": "YAML",
    ".yml": "YAML",
    ".toml": "TOML",
    ".json": "JSON",
}

FRAMEWORK_HINTS = {
    "django": "Django",
    "fastapi": "FastAPI",
    "flask": "Flask",
    "react": "React",
    "next": "Next.js",
    "typer": "Typer",
    "sqlalchemy": "SQLAlchemy",
}


def scan_repository(repo_path: Path, repository_id: str | None = None) -> RepositoryMetadata:
    repo_path = repo_path.resolve()
    if not repo_path.is_dir():
        raise RepositoryError(f"Path does not exist: {repo_path}")
    try:
        git = Repo(repo_path)
    except InvalidGitRepositoryError as exc:
        raise RepositoryError(f"Not a git repository: {repo_path}") from exc

    remote_url = None
    if git.remotes:
        try:
            remote_url = git.remotes.origin.url
        except Exception:
            remote_url = None

    gitignore_spec = _load_gitignore(repo_path)
    lang_counter: Counter[str] = Counter()
    file_count: Counter[str] = Counter()

    for file_path in repo_path.rglob("*"):
        if not file_path.is_file():
            continue
        rel = str(file_path.relative_to(repo_path))
        if _ignored(rel, gitignore_spec):
            continue
        if is_sensitive_path(rel):
            continue
        ext = file_path.suffix.lower()
        lang = EXT_LANGUAGE.get(ext, "Other")
        if lang != "Other":
            lang_counter[lang] += 1
            file_count[lang] += 1

    languages = [
        LanguageStat(language=lang, file_count=file_count[lang], byte_estimate=0)
        for lang, _ in lang_counter.most_common()
    ]
    primary = languages[0].language if languages else None

    dependencies = _detect_dependencies(repo_path)
    frameworks = _detect_frameworks(repo_path, dependencies)
    documentation = scan_documentation(repo_path)
    architecture = scan_architecture(repo_path)
    infrastructure = _detect_infrastructure(repo_path)

    head_sha = git.head.commit.hexsha if git.head.commit else None

    return RepositoryMetadata(
        id=repository_id or str(uuid4()),
        name=repo_path.name,
        path=str(repo_path),
        remote_url=remote_url,
        primary_language=primary,
        languages=languages,
        frameworks=frameworks,
        dependencies=dependencies,
        architecture=architecture,
        documentation=documentation,
        infrastructure=infrastructure,
        last_analyzed_commit=head_sha,
        analyzed_at=datetime.now(timezone.utc).replace(tzinfo=None),
    )


def _load_gitignore(repo_path: Path) -> PathSpec | None:
    gi = repo_path / ".gitignore"
    if not gi.is_file():
        return None
    lines = gi.read_text(encoding="utf-8", errors="ignore").splitlines()
    return PathSpec.from_lines(GitWildMatchPattern, lines)


def _ignored(rel: str, spec: PathSpec | None) -> bool:
    if rel.startswith(".git/"):
        return True
    return bool(spec and spec.match_file(rel))


def _detect_dependencies(repo_path: Path) -> list[DependencySet]:
    sets: list[DependencySet] = []
    pyproject = repo_path / "pyproject.toml"
    if pyproject.is_file():
        deps = _parse_pyproject_deps(pyproject.read_text(encoding="utf-8", errors="ignore"))
        if deps:
            sets.append(DependencySet(ecosystem="python", dependencies=deps))
    pkg = repo_path / "package.json"
    if pkg.is_file():
        try:
            data = json.loads(pkg.read_text(encoding="utf-8"))
            deps = list((data.get("dependencies") or {}).keys())[:50]
            if deps:
                sets.append(DependencySet(ecosystem="npm", dependencies=deps))
        except json.JSONDecodeError:
            pass
    gomod = repo_path / "go.mod"
    if gomod.is_file():
        deps = [
            ln.strip().split()[0]
            for ln in gomod.read_text(encoding="utf-8", errors="ignore").splitlines()
            if ln.strip().startswith("require ")
            or (ln.strip() and "\t" in ln and "require" not in ln)
        ][:50]
        if deps:
            sets.append(DependencySet(ecosystem="go", dependencies=deps))
    return sets


def _parse_pyproject_deps(text: str) -> list[str]:
    deps: list[str] = []
    in_deps = False
    for line in text.splitlines():
        if line.strip().startswith("dependencies") and "[" in line:
            in_deps = True
            continue
        if in_deps:
            if line.strip() == "]":
                break
            m = re.search(r'"([^"]+)"', line)
            if m:
                name = re.split(r"[<>=!~\[]", m.group(1))[0].strip()
                deps.append(name)
    return deps[:50]


def _detect_frameworks(repo_path: Path, deps: list[DependencySet]) -> list[str]:
    found: set[str] = set()
    corpus = ""
    for dset in deps:
        corpus += " ".join(dset.dependencies).lower()
    for key, label in FRAMEWORK_HINTS.items():
        if key in corpus:
            found.add(label)
    return sorted(found)


def _detect_infrastructure(repo_path: Path) -> InfrastructureHints:
    ci: list[str] = []
    configs: list[str] = []
    gh = repo_path / ".github" / "workflows"
    if gh.is_dir():
        ci.append("GitHub Actions")
        for wf in gh.glob("*.yml"):
            configs.append(str(wf.relative_to(repo_path)))
    if (repo_path / ".gitlab-ci.yml").is_file():
        ci.append("GitLab CI")
        configs.append(".gitlab-ci.yml")
    if (repo_path / "Dockerfile").is_file():
        configs.append("Dockerfile")
    if (repo_path / "docker-compose.yml").is_file():
        configs.append("docker-compose.yml")
    return InfrastructureHints(ci_systems=ci, config_files=configs)
