from pathlib import Path

from typer.testing import CliRunner

from skald.core.config import resolve_config
from skald.core.container import build_context
from skald.main import app

runner = CliRunner()


def test_end_to_end_cli(skald_home: Path, sample_repo: Path, tmp_path: Path, monkeypatch) -> None:
    config_path = tmp_path / "config" / "config.yaml"
    monkeypatch.setenv("SKALD_WORKSPACE", str(skald_home))
    assert runner.invoke(app, ["init", "--config", str(config_path)]).exit_code == 0

    assert runner.invoke(app, ["scan", "repo", str(sample_repo)]).exit_code == 0
    assert runner.invoke(app, ["scan", "git", str(sample_repo), "--limit", "50"]).exit_code == 0
    assert runner.invoke(app, ["analyze"]).exit_code == 0

    list_result = runner.invoke(app, ["features", "list"])
    assert list_result.exit_code == 0
    assert list_result.stdout.strip()

    ctx = build_context()
    features = ctx.knowledge.list_features()
    fid = features[0].id

    show = runner.invoke(app, ["features", "show", fid])
    assert show.exit_code == 0
    assert features[0].title[:20] in show.stdout or "feat" in show.stdout

    export = runner.invoke(app, ["features", "export", fid, "--format", "yaml"])
    assert export.exit_code == 0
    assert Path(skald_home / "features" / f"{fid}.yaml").is_file()

    draft = runner.invoke(app, ["content", "draft", fid, "--format", "article"])
    assert draft.exit_code == 0
    cfg = resolve_config(config_path)
    drafts = list(cfg.content.output_directory.glob("*.md"))
    assert drafts
    text = drafts[0].read_text(encoding="utf-8")
    assert features[0].related_commits[0][:8] in text or "Implementation evidence" in text

    report = runner.invoke(app, ["report"])
    assert report.exit_code == 0
    assert "Repositories analyzed" in report.stdout
