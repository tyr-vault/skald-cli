"""Architecture pattern heuristics."""

from __future__ import annotations

from pathlib import Path

from skald.schemas.repository import ArchitectureHints

LAYER_DIRS = ("domain", "application", "infrastructure", "adapters", "interfaces", "core")
PATTERN_MARKERS = {
    "layered": ("domain", "infrastructure"),
    "hexagonal": ("adapters", "ports"),
    "mvc": ("models", "views", "controllers"),
}


def scan_architecture(repo_path: Path) -> ArchitectureHints:
    names = {p.name.lower() for p in repo_path.iterdir() if p.is_dir()}
    patterns: list[str] = []
    layers: list[str] = []
    evidence: list[str] = []

    for layer in LAYER_DIRS:
        if layer in names:
            layers.append(layer)
            evidence.append(f"top-level directory: {layer}/")

    for pattern, required in PATTERN_MARKERS.items():
        if all(r in names for r in required):
            patterns.append(pattern)
            evidence.append(f"directories suggest {pattern}: {', '.join(required)}")

    return ArchitectureHints(patterns=patterns, layers=layers, evidence=evidence)
