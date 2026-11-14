# Development

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

Python 3.11+ is recommended; the project metadata allows 3.10+ for broader environments.

## Quality gates

```bash
pytest
ruff check src tests
ruff format src tests
mypy src/skald
```

## Layout

- `src/skald/` — application code (`skald` CLI entry point)
- `tests/` — unit + integration (temp git repos)
- `examples/sample-repo/` — demo repository with commit history

## Adding a provider

1. Implement the port in `domain/ports.py` (or extend `providers/`).
2. Wire it in `core/container.py` or the relevant use case.
3. Keep CLI commands thin; add tests with fixtures.
