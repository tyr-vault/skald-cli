"""Simple dependency wiring."""

from __future__ import annotations

from dataclasses import dataclass

from sqlalchemy.orm import Session, sessionmaker

from skald.analysis.knowledge_extraction import KnowledgeExtractor
from skald.core.config import SkaldConfig, resolve_config
from skald.providers.llm.mock import MockLLMProvider
from skald.storage.database import get_session_factory
from skald.storage.repositories import KnowledgeRepository


@dataclass
class AppContext:
    config: SkaldConfig
    session_factory: sessionmaker[Session]
    knowledge: KnowledgeRepository
    knowledge_extractor: KnowledgeExtractor

    @property
    def workspace(self) -> str:
        return str(self.config.workspace.path)


def build_context(config_path: str | None = None) -> AppContext:
    from pathlib import Path

    cfg = resolve_config(Path(config_path) if config_path else None)
    factory = get_session_factory(cfg.storage.database)
    knowledge = KnowledgeRepository(factory)
    llm = MockLLMProvider()
    extractor = KnowledgeExtractor(llm)
    return AppContext(
        config=cfg,
        session_factory=factory,
        knowledge=knowledge,
        knowledge_extractor=extractor,
    )
