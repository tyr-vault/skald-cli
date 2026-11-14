# Skald architecture

Skald is a **local-first knowledge extraction pipeline**. It is not a generic Git dashboard or an automatic article bot.

Brand asset: [`../public/favicon.ico`](../public/favicon.ico).

## Pipeline overview

```mermaid
flowchart LR
  RepoScan[RepositoryScanner]
  GitScan[GitScanner]
  Norm[Normalization]
  Feat[FeatureDiscovery]
  Know[KnowledgeExtraction]
  DB[(SQLiteCatalog)]
  Out[ContentDrafts_Reports]

  RepoScan --> Norm
  GitScan --> Norm
  Norm --> Feat
  Feat --> Know
  Know --> DB
  DB --> Out
```

## System context

```mermaid
flowchart TB
  Dev[Developer]

  subgraph cli [CLI_skald]
    Commands[init_scan_analyze_features_content_report]
  end

  subgraph app [Application_UseCases]
    UC[init_workspace_scan_analyze_draft_report]
  end

  subgraph domain [Domain]
    Group[CommitGrouping]
    Ports[PortProtocols]
  end

  subgraph infra [Infrastructure]
    LocalGit[GitPython_Local]
    GH[GitHub_HTTP_Listing]
    LLM[Mock_LLM_Provider]
    Store[SQLAlchemy_SQLite]
    Files[Workspace_Artifacts]
  end

  ExtRepo[Local_Git_Repo]
  ExtGH[GitHub_API]

  Dev --> Commands
  Commands --> UC
  UC --> Group
  UC --> Ports
  UC --> Store
  UC --> Files
  LocalGit --> ExtRepo
  GH --> ExtGH
  Ports --> LocalGit
  Ports --> GH
  Ports --> LLM
  Store --> Files
```

## CLI to use-case flow

```mermaid
sequenceDiagram
  participant Dev as Developer
  participant CLI as skald_CLI
  participant App as Application
  participant Git as LocalGitProvider
  participant DB as SQLite

  Dev->>CLI: skald init
  CLI->>App: init_workspace
  App->>DB: create schema

  Dev->>CLI: skald scan repo PATH
  CLI->>App: scan_repository
  App->>Git: inspect tree
  App->>DB: upsert repository

  Dev->>CLI: skald scan git PATH
  CLI->>App: scan_git
  App->>Git: walk commits
  App->>DB: upsert commits

  Dev->>CLI: skald analyze
  CLI->>App: analyze
  App->>DB: group features + extract metadata

  Dev->>CLI: skald content draft ID
  CLI->>App: generate_draft
  App->>DB: load feature
  App-->>Dev: Markdown under workspace
```

## Layers (DDD)

| Layer | Responsibility |
|-------|----------------|
| `cli/` | Typer adapters; no business logic |
| `application/` | Use cases (init, scan, analyze, content, report) |
| `domain/` | Pure grouping logic and port protocols |
| `scanners/`, `providers/`, `storage/` | Infrastructure adapters |
| `schemas/` | Pydantic contracts (JSON/YAML) |

```mermaid
flowchart TB
  CLI[cli]
  APP[application]
  DOM[domain]
  SCH[schemas]
  INF[scanners_providers_storage]

  CLI --> APP
  APP --> DOM
  APP --> SCH
  APP --> INF
  INF --> DOM
```

## Extension points

- `providers/git/local.py` — GitPython
- `providers/git/github.py` — public repo listing (commits/PR sync planned)
- `providers/llm/mock.py` — offline enrichment; swap for a real LLM provider
- `analysis/commit_grouping.py` — `SemanticGroupingStrategy` placeholder

## Persistence

- SQLite via SQLAlchemy (`storage/models.py`)
- Artifacts: diffs, exported YAML, generated Markdown under workspace
- Alembic scaffold in `alembic/` (schema also created on init via metadata)

## Security

- Sensitive paths (`.env`, keys, secrets patterns) excluded from scans
- GitHub tokens read from environment only; never logged
