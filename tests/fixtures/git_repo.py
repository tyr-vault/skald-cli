"""Create temporary git repositories for tests."""

from __future__ import annotations

from pathlib import Path

from git import Repo


def create_sample_repo(path: Path) -> Repo:
    path.mkdir(parents=True, exist_ok=True)
    repo = Repo.init(path)
    with repo.config_writer() as cw:
        cw.set_value("user", "name", "Test User")
        cw.set_value("user", "email", "test@example.com")

    readme = path / "README.md"
    readme.write_text("# Sample\n\nA tiny example service.\n", encoding="utf-8")
    repo.index.add(["README.md"])
    repo.index.commit("feat: add readme and project scaffold")

    src = path / "src" / "app.py"
    src.parent.mkdir(parents=True, exist_ok=True)
    src.write_text("def hello():\n    return 'hello'\n", encoding="utf-8")
    repo.index.add(["src/app.py"])
    repo.index.commit("feat: implement hello endpoint in app module")

    test = path / "tests" / "test_app.py"
    test.parent.mkdir(parents=True, exist_ok=True)
    test.write_text("def test_hello():\n    assert True\n", encoding="utf-8")
    repo.index.add(["tests/test_app.py"])
    repo.index.commit("test: add unit test for app module")

    return repo
