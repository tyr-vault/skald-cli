"""Knowledge extraction from features and evidence."""

from __future__ import annotations

from skald.domain.ports import LLMCompleter
from skald.schemas.commit import CommitMetadata
from skald.schemas.feature import (
    FeatureMetadata,
    LearningOpportunity,
    SourceRef,
    TechnicalConcept,
)
from skald.schemas.repository import RepositoryMetadata


class KnowledgeExtractor:
    def __init__(self, llm: LLMCompleter) -> None:
        self._llm = llm

    def enrich(
        self,
        feature: FeatureMetadata,
        commits: list[CommitMetadata],
        repository: RepositoryMetadata | None,
    ) -> FeatureMetadata:
        prompt = self._build_prompt(feature, commits, repository)
        llm_out = self._llm.complete_json(prompt, schema_hint="feature_enrichment")

        problem = str(llm_out.get("problem", "undocumented"))
        motivation = str(llm_out.get("motivation", "undocumented"))
        solution = str(llm_out.get("solution", "undocumented"))

        if problem == "undocumented":
            problem = _observed_problem(commits)
        if motivation == "undocumented":
            motivation = motivation
        if solution == "undocumented":
            solution = _observed_solution(commits)

        concepts = _observed_concepts(commits, repository)
        learning = _learning_opportunities(commits)

        feature.problem = problem
        feature.motivation = motivation
        feature.solution = solution
        feature.technical_concepts = concepts
        feature.learning_opportunities = learning
        if repository:
            feature.technologies = sorted(set(feature.technologies) | set(repository.frameworks))
            if (
                repository.primary_language
                and repository.primary_language not in feature.technologies
            ):
                feature.technologies.append(repository.primary_language)
        return feature

    def _build_prompt(
        self,
        feature: FeatureMetadata,
        commits: list[CommitMetadata],
        repository: RepositoryMetadata | None,
    ) -> str:
        msgs = "\n".join(c.message.splitlines()[0] for c in commits[:10])
        repo_name = repository.name if repository else "unknown"
        return f"Repository: {repo_name}\nFeature: {feature.title}\nCommits:\n{msgs}"


def _observed_problem(commits: list[CommitMetadata]) -> str:
    for c in commits:
        first = c.message.splitlines()[0].lower()
        if first.startswith("fix"):
            return f"Commit message indicates a fix: {c.message.splitlines()[0]}"
    return "undocumented"


def _observed_solution(commits: list[CommitMetadata]) -> str:
    files = sorted({cf.path for c in commits for cf in c.changed_files})[:10]
    if files:
        return "Changes observed in: " + ", ".join(files)
    return "undocumented"


def _observed_concepts(
    commits: list[CommitMetadata],
    repository: RepositoryMetadata | None,
) -> list[TechnicalConcept]:
    concepts: list[TechnicalConcept] = []
    if repository:
        for fw in repository.frameworks:
            concepts.append(
                TechnicalConcept(
                    name=fw,
                    description="Detected from repository dependencies.",
                    sources=[SourceRef(kind="observed", note="repository scan")],
                )
            )
    for c in commits[:5]:
        concepts.append(
            TechnicalConcept(
                name=c.message.splitlines()[0][:80],
                description="Referenced in commit history.",
                sources=[SourceRef(commit_sha=c.sha, kind="observed")],
            )
        )
    return concepts


def _learning_opportunities(commits: list[CommitMetadata]) -> list[LearningOpportunity]:
    topics: list[LearningOpportunity] = []
    for c in commits:
        if len(c.changed_files) > 3:
            topics.append(
                LearningOpportunity(
                    topic="Multi-file change review",
                    description=f"Review commit {c.sha[:8]} touching {len(c.changed_files)} files.",
                    sources=[SourceRef(commit_sha=c.sha, kind="observed")],
                )
            )
    return topics[:5]
