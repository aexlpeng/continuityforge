from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

HUMAN_DIMENSIONS = (
    "character_identity",
    "scene_and_prop_continuity",
    "motion_plausibility",
    "dialogue_alignment",
    "narrative_coherence",
    "visual_artifact_control",
)


def automatic_checks(manifest: dict[str, Any]) -> dict[str, Any]:
    shots = manifest.get("shots", [])
    valid_durations = all(item.get("shot", {}).get("duration_seconds") in (5, 10) for item in shots)
    has_states = all(
        isinstance(item.get("shot", {}).get("start_state"), dict)
        and isinstance(item.get("shot", {}).get("end_state"), dict)
        for item in shots
    )
    completed = sum(item.get("generation", {}).get("status") == "completed" for item in shots)
    dry_runs = sum(item.get("generation", {}).get("status") == "dry-run" for item in shots)
    return {
        "shot_count": len(shots),
        "valid_duration_windows": valid_durations,
        "all_shots_have_state_contracts": has_states,
        "completed_shots": completed,
        "dry_run_shots": dry_runs,
        "completion_rate": completed / len(shots) if shots else 0.0,
    }


def blank_evaluation(manifest: dict[str, Any]) -> dict[str, Any]:
    return {
        "schema_version": "0.1",
        "created_at": datetime.now(timezone.utc).isoformat(),
        "episode_id": manifest.get("episode_id"),
        "manifest_created_at": manifest.get("created_at"),
        "automatic": automatic_checks(manifest),
        "human_rubric": {
            "scale": "1=unusable, 2=major defects, 3=acceptable, 4=strong, 5=excellent",
            "minimum_raters_recommended": 3,
            "dimensions": list(HUMAN_DIMENSIONS),
        },
        "shots": [
            {
                "shot_id": item.get("shot", {}).get("id"),
                "rater_id": None,
                "scores": {dimension: None for dimension in HUMAN_DIMENSIONS},
                "failure_labels": [],
                "notes": "",
            }
            for item in manifest.get("shots", [])
        ],
    }

