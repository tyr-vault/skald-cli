"""Pytest fixtures."""

from __future__ import annotations

import os
from pathlib import Path

import pytest

from fixtures.git_repo import create_sample_repo
from skald.application.init_workspace import init_workspace
from skald.core.config import ContentSettings, SkaldConfig, StorageSettings, WorkspaceSettings


@pytest.fixture
def skald_home(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    workspace = tmp_path / "workspace"
    config_dir = tmp_path / "config"
    config_path = config_dir / "config.yaml"
    monkeypatch.setenv("SKALD_WORKSPACE", str(workspace))
    cfg = SkaldConfig(
        workspace=WorkspaceSettings(path=workspace),
        storage=StorageSettings(database=workspace / "skald.db"),
        content=ContentSettings(output_directory=workspace / "content"),
    )
    init_workspace(cfg, config_path)
    monkeypatch.setenv("HOME", str(tmp_path))
    os.environ["SKALD_WORKSPACE"] = str(workspace)
    return workspace


@pytest.fixture
def sample_repo(tmp_path: Path) -> Path:
    repo_path = tmp_path / "repo"
    create_sample_repo(repo_path)
    return repo_path
