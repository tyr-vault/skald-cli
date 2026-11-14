"""JSON/YAML serialization helpers."""

from __future__ import annotations

from pathlib import Path
from typing import Any, TypeVar

import yaml
from pydantic import BaseModel

T = TypeVar("T", bound=BaseModel)


def to_yaml(model: BaseModel) -> str:
    return yaml.safe_dump(
        model.model_dump(mode="json"),
        sort_keys=False,
        allow_unicode=True,
    )


def to_json_dict(model: BaseModel) -> dict[str, Any]:
    return model.model_dump(mode="json")


def write_yaml(path: Path, model: BaseModel) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(to_yaml(model), encoding="utf-8")


def load_yaml(path: Path, model_type: type[T]) -> T:
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    return model_type.model_validate(data)
