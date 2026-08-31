from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml

from .errors import RoutingError, ValidationError
from .models import Shot


@dataclass(frozen=True)
class ModelConfig:
    id: str
    endpoint: str
    tasks: tuple[str, ...]
    durations: tuple[int, ...]
    priority: int = 100
    estimated_cost_per_second_usd: float | None = None
    arguments: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, data: dict[str, Any], context: str) -> ModelConfig:
        required = ("id", "endpoint", "tasks", "durations")
        missing = [key for key in required if not data.get(key)]
        if missing:
            raise ValidationError(f"{context} is missing: {', '.join(missing)}")
        durations = tuple(int(value) for value in data["durations"])
        if any(value not in (5, 10) for value in durations):
            raise ValidationError(f"{context}.durations may only contain 5 and 10")
        return cls(
            id=str(data["id"]),
            endpoint=str(data["endpoint"]),
            tasks=tuple(str(value) for value in data["tasks"]),
            durations=durations,
            priority=int(data.get("priority", 100)),
            estimated_cost_per_second_usd=(
                float(data["estimated_cost_per_second_usd"])
                if data.get("estimated_cost_per_second_usd") is not None
                else None
            ),
            arguments=dict(data.get("arguments", {})),
        )


class ModelRouter:
    def __init__(self, models: list[ModelConfig]) -> None:
        if not models:
            raise ValidationError("Model configuration must include at least one model")
        self.models = models

    @classmethod
    def load(cls, path: str | Path) -> ModelRouter:
        with Path(path).open("r", encoding="utf-8") as handle:
            data = yaml.safe_load(handle)
        if not isinstance(data, dict) or not isinstance(data.get("models"), list):
            raise ValidationError("Model config must contain a 'models' list")
        return cls(
            [
                ModelConfig.from_dict(item, f"models[{index}]")
                for index, item in enumerate(data["models"])
            ]
        )

    def route(self, shot: Shot) -> ModelConfig:
        candidates = [
            model
            for model in self.models
            if shot.task in model.tasks and shot.duration_seconds in model.durations
        ]
        if not candidates:
            raise RoutingError(
                f"No model supports task={shot.task!r}, duration={shot.duration_seconds}s"
            )
        return sorted(
            candidates,
            key=lambda model: (
                model.priority,
                model.estimated_cost_per_second_usd
                if model.estimated_cost_per_second_usd is not None
                else float("inf"),
                model.id,
            ),
        )[0]

