from __future__ import annotations

import json
from dataclasses import asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .generation import DryRunClient, FalClient, GenerationClient
from .models import Episode, Shot
from .planner import plan_episode
from .router import ModelRouter


def write_json(path: str | Path, data: Any) -> Path:
    destination = Path(path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    with destination.open("w", encoding="utf-8") as handle:
        json.dump(data, handle, ensure_ascii=False, indent=2)
        handle.write("\n")
    return destination


def plan_to_directory(episode: Episode, output_dir: str | Path) -> tuple[list[Shot], Path]:
    shots = plan_episode(episode)
    path = write_json(
        Path(output_dir) / "storyboard.json",
        {
            "schema_version": "0.1",
            "episode_id": episode.id,
            "title": episode.title,
            "total_duration_seconds": sum(shot.duration_seconds for shot in shots),
            "shots": [shot.to_dict() for shot in shots],
        },
    )
    return shots, path


def generate_to_directory(
    episode: Episode,
    router: ModelRouter,
    output_dir: str | Path,
    dry_run: bool = True,
    client_timeout: float | None = None,
) -> Path:
    shots, storyboard_path = plan_to_directory(episode, output_dir)
    client: GenerationClient = DryRunClient() if dry_run else FalClient(client_timeout)
    rows: list[dict[str, Any]] = []
    for shot in shots:
        model = router.route(shot)
        result = client.generate(model, shot)
        rows.append(
            {
                "shot": shot.to_dict(),
                "model": asdict(model),
                "generation": result.to_dict(),
            }
        )

    manifest = {
        "schema_version": "0.1",
        "created_at": datetime.now(timezone.utc).isoformat(),
        "episode_id": episode.id,
        "mode": "dry-run" if dry_run else "live",
        "storyboard": str(storyboard_path),
        "shots": rows,
    }
    return write_json(Path(output_dir) / "manifest.json", manifest)

