"""Configuration loading and defaults."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml
from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings, SettingsConfigDict

from skald.core.exceptions import ConfigurationError


def _expand_path(value: str | Path) -> Path:
    return Path(value).expanduser().resolve()


class WorkspaceSettings(BaseModel):
    path: Path = Field(default_factory=lambda: _expand_path("~/.devlog"))


class StorageSettings(BaseModel):
    database: Path = Field(default_factory=lambda: _expand_path("~/.devlog/skald.db"))


class AnalysisSettings(BaseModel):
    max_diff_size: int = 50_000
    default_history_limit: int = 1000
    grouping_window_hours: int = 72
    minimum_group_confidence: float = 0.65
    message_weight: float = 0.3
    temporal_weight: float = 0.1
    file_weight: float = 0.3
    directory_weight: float = 0.2
    concept_weight: float = 0.1


class GitHubSettings(BaseModel):
    token_env: str = "GITHUB_TOKEN"


class LLMSettings(BaseModel):
    provider: str = "mock"
    model: str | None = None


class ContentSettings(BaseModel):
    default_language: str = "en"
    output_directory: Path = Field(default_factory=lambda: _expand_path("~/.devlog/content"))


class SkaldConfig(BaseModel):
    workspace: WorkspaceSettings = Field(default_factory=WorkspaceSettings)
    storage: StorageSettings = Field(default_factory=StorageSettings)
    analysis: AnalysisSettings = Field(default_factory=AnalysisSettings)
    github: GitHubSettings = Field(default_factory=GitHubSettings)
    llm: LLMSettings = Field(default_factory=LLMSettings)
    content: ContentSettings = Field(default_factory=ContentSettings)


class EnvSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="SKALD_", extra="ignore")

    workspace: Path | None = None


DEFAULT_CONFIG_PATH = Path("~/.config/devlog/config.yaml")


def default_config_dict() -> dict[str, Any]:
    cfg = SkaldConfig()
    return {
        "workspace": {"path": str(cfg.workspace.path)},
        "storage": {"database": str(cfg.storage.database)},
        "analysis": cfg.analysis.model_dump(),
        "github": cfg.github.model_dump(),
        "llm": cfg.llm.model_dump(),
        "content": {
            "default_language": cfg.content.default_language,
            "output_directory": str(cfg.content.output_directory),
        },
    }


def load_config_file(path: Path) -> SkaldConfig:
    if not path.is_file():
        raise ConfigurationError(f"Config file not found: {path}")
    with path.open(encoding="utf-8") as f:
        raw = yaml.safe_load(f) or {}
    return SkaldConfig.model_validate(raw)


def resolve_config(config_path: Path | None = None) -> SkaldConfig:
    env = EnvSettings()
    path = (config_path or DEFAULT_CONFIG_PATH.expanduser()).resolve()
    cfg = load_config_file(path) if path.is_file() else SkaldConfig()
    if env.workspace is not None:
        cfg.workspace.path = _expand_path(env.workspace)
        cfg.storage.database = cfg.workspace.path / "skald.db"
        cfg.content.output_directory = cfg.workspace.path / "content"
    return cfg


def config_file_path() -> Path:
    return DEFAULT_CONFIG_PATH.expanduser().resolve()


def is_initialized() -> bool:
    env = EnvSettings()
    if env.workspace is not None:
        return (_expand_path(env.workspace) / "skald.db").is_file()
    path = config_file_path()
    if not path.is_file():
        return False
    try:
        cfg = load_config_file(path)
    except ConfigurationError:
        return False
    return cfg.storage.database.is_file()


def write_default_config(path: Path | None = None) -> Path:
    target = (path or config_file_path()).expanduser()
    target.parent.mkdir(parents=True, exist_ok=True)
    with target.open("w", encoding="utf-8") as f:
        yaml.safe_dump(default_config_dict(), f, sort_keys=False)
    return target.resolve()
