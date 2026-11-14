"""Hashing utilities."""

from __future__ import annotations

import hashlib


def short_hash(value: str, length: int = 12) -> str:
    return hashlib.sha256(value.encode()).hexdigest()[:length]
