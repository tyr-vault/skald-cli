"""Sensitive path and content guards."""

from __future__ import annotations

import re
from pathlib import PurePosixPath

SENSITIVE_NAMES = {
    ".env",
    ".env.local",
    ".env.production",
    "credentials.json",
    "secrets.yaml",
    "id_rsa",
    "id_ed25519",
}

SENSITIVE_PATTERNS = [
    re.compile(r"\.pem$", re.I),
    re.compile(r"secret", re.I),
    re.compile(r"password", re.I),
    re.compile(r"token", re.I),
]


def is_sensitive_path(path: str) -> bool:
    name = PurePosixPath(path.replace("\\", "/")).name
    if name in SENSITIVE_NAMES or name.startswith(".env"):
        return True
    return any(p.search(path) for p in SENSITIVE_PATTERNS)
