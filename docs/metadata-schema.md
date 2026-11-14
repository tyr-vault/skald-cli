# Metadata schema

Domain models live in `src/skald/schemas/` as Pydantic v2 models.

## RepositoryMetadata

Repository structure, languages, dependencies, architecture hints, documentation refs, CI/infrastructure signals, `last_analyzed_commit`, `analyzed_at`.

## CommitMetadata

SHA, author, timestamps, message, per-file changes, stats, `diff_reference` (filesystem path to truncated patch), parents, merge flag.

## FeatureMetadata

Engineering feature with evidence:

- `related_commits`, `related_files`
- Nested: `implementation_steps`, `architectural_decisions`, `tradeoffs`, `technical_concepts`, `learning_opportunities`
- `SourceRef` with `kind`: `observed` | `inferred`
- `confidence`, `status` (`discovered` | `needs_review` | `documented`)

Unknown facts are stored as `null` or the string `undocumented`.

## ContentMetadata

Links a feature to a generated draft (`article`, `learning-note`, `linkedin`), output path, language, status.

## Serialization

Use `schemas/serialization.py` for YAML export (`skald features export`).
