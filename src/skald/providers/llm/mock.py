"""Mock LLM for tests and offline MVP."""

from __future__ import annotations

import re


class MockLLMProvider:
    def complete_json(self, prompt: str, schema_hint: str) -> dict[str, object]:
        """Return minimal structured enrichment without inventing code details."""
        motivation = "undocumented"
        if re.search(r"\bfix\b", prompt, re.I):
            motivation = "Address a defect described in commit messages."
        elif re.search(r"\bfeat\b", prompt, re.I):
            motivation = "Introduce capability described in commit messages."
        return {
            "motivation": motivation,
            "problem": "undocumented",
            "solution": "See related commits and changed files for implementation evidence.",
            "inferred": True,
            "schema_hint": schema_hint,
            "prompt_length": len(prompt),
        }
