from pathlib import Path

import yaml

from skald.core.config import SkaldConfig, load_config_file, write_default_config


def test_write_and_load_config(tmp_path: Path) -> None:
    path = tmp_path / "config.yaml"
    write_default_config(path)
    cfg = load_config_file(path)
    assert isinstance(cfg, SkaldConfig)
    assert cfg.analysis.default_history_limit == 1000


def test_yaml_roundtrip(tmp_path: Path) -> None:
    path = tmp_path / "config.yaml"
    write_default_config(path)
    data = yaml.safe_load(path.read_text())
    assert "workspace" in data
