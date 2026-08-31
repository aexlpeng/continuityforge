import json
from pathlib import Path

from continuityforge.evaluator import blank_evaluation
from continuityforge.models import Episode
from continuityforge.pipeline import generate_to_directory
from continuityforge.router import ModelRouter

ROOT = Path(__file__).parents[1]
EPISODE = ROOT / "examples" / "episode-001" / "episode.yaml"
CONFIG = ROOT / "configs" / "models.example.yaml"


def test_dry_run_writes_reproducible_manifest(tmp_path: Path) -> None:
    manifest_path = generate_to_directory(
        Episode.load(EPISODE), ModelRouter.load(CONFIG), tmp_path, dry_run=True
    )
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    assert manifest["mode"] == "dry-run"
    assert len(manifest["shots"]) == 5
    assert all(row["generation"]["status"] == "dry-run" for row in manifest["shots"])
    first_prompt = manifest["shots"][0]["generation"]["response"]["arguments"]["prompt"]
    assert "Create one continuous" in first_prompt

    evaluation = blank_evaluation(manifest)
    assert evaluation["automatic"]["valid_duration_windows"] is True
    assert evaluation["automatic"]["dry_run_shots"] == 5
