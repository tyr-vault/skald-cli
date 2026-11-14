"""GitHub API provider (read-only listing)."""

from __future__ import annotations

import os
from typing import Any

import httpx

from skald.core.exceptions import RepositoryError
from skald.core.logging import get_logger

logger = get_logger(__name__)

GITHUB_API = "https://api.github.com"


class GitHubProvider:
    def __init__(self, token_env: str = "GITHUB_TOKEN") -> None:
        self._token_env = token_env

    def _headers(self) -> dict[str, str]:
        token = os.environ.get(self._token_env, "")
        headers = {"Accept": "application/vnd.github+json", "User-Agent": "skald-cli"}
        if token:
            headers["Authorization"] = f"Bearer {token}"
        return headers

    def list_public_repositories(self, username: str) -> list[dict[str, Any]]:
        url = f"{GITHUB_API}/users/{username}/repos"
        repos: list[dict[str, Any]] = []
        page = 1
        with httpx.Client(timeout=30.0) as client:
            while True:
                response = client.get(
                    url,
                    headers=self._headers(),
                    params={"per_page": 100, "page": page, "type": "owner"},
                )
                if response.status_code == 403:
                    raise RepositoryError(
                        "GitHub API rate limit or forbidden. Set GITHUB_TOKEN for higher limits."
                    )
                if response.status_code == 404:
                    raise RepositoryError(f"GitHub user not found: {username}")
                response.raise_for_status()
                batch = response.json()
                if not batch:
                    break
                repos.extend(batch)
                if len(batch) < 100:
                    break
                page += 1
        # Never log tokens
        logger.info("Listed %s public repositories for user %s", len(repos), username)
        return repos
