from __future__ import annotations

import os
from dataclasses import asdict, dataclass
from typing import Any, Protocol

from .errors import GenerationError
from .models import Shot
from .router import ModelConfig


@dataclass(frozen=True)
class GenerationResult:
    status: str
    provider: str
    model_id: str
    endpoint: str
    request_id: str | None
    response: dict[str, Any]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


class GenerationClient(Protocol):
    def generate(self, model: ModelConfig, shot: Shot) -> GenerationResult: ...


def render_arguments(template: dict[str, Any], shot: Shot) -> dict[str, Any]:
    replacements = {
        "{prompt}": shot.prompt,
        "{negative_prompt}": shot.negative_prompt,
        "{duration_seconds}": shot.duration_seconds,
        "{shot_id}": shot.id,
    }

    def replace(value: Any) -> Any:
        if isinstance(value, dict):
            return {key: replace(item) for key, item in value.items()}
        if isinstance(value, list):
            return [replace(item) for item in value]
        if isinstance(value, str):
            if value in replacements:
                return replacements[value]
            rendered = value
            for token, replacement in replacements.items():
                rendered = rendered.replace(token, str(replacement))
            return rendered
        return value

    return replace(template)


class DryRunClient:
    def generate(self, model: ModelConfig, shot: Shot) -> GenerationResult:
        return GenerationResult(
            status="dry-run",
            provider="fal",
            model_id=model.id,
            endpoint=model.endpoint,
            request_id=None,
            response={"arguments": render_arguments(model.arguments, shot)},
        )


class FalClient:
    """Thin adapter around fal-client's queue-backed subscribe call."""

    def __init__(self, client_timeout: float | None = None) -> None:
        if not os.environ.get("FAL_KEY"):
            raise GenerationError("FAL_KEY is not set; use --dry-run or export a scoped key")
        try:
            import fal_client
        except ImportError as exc:
            raise GenerationError(
                "fal-client is not installed; run: python -m pip install -e \".[fal]\""
            ) from exc
        self._client = fal_client
        self._client_timeout = client_timeout

    def generate(self, model: ModelConfig, shot: Shot) -> GenerationResult:
        request_id: str | None = None

        def on_enqueue(value: str) -> None:
            nonlocal request_id
            request_id = value

        try:
            response = self._client.subscribe(
                model.endpoint,
                arguments=render_arguments(model.arguments, shot),
                with_logs=True,
                on_enqueue=on_enqueue,
                client_timeout=self._client_timeout,
            )
        except Exception as exc:
            raise GenerationError(
                f"fal generation failed for {shot.id} via {model.id}: {exc}"
            ) from exc
        return GenerationResult(
            status="completed",
            provider="fal",
            model_id=model.id,
            endpoint=model.endpoint,
            request_id=request_id,
            response=dict(response),
        )

