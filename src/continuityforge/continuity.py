from __future__ import annotations

from typing import Any

from .models import Beat, Character, Episode, Scene

DEFAULT_NEGATIVE_PROMPT = (
    "identity drift, wardrobe change, duplicate character, disappearing prop, "
    "location reset, camera jump, text artifacts, deformed hands, lip-sync mismatch"
)


def merge_state(*states: dict[str, Any]) -> dict[str, Any]:
    merged: dict[str, Any] = {}
    for state in states:
        merged.update(state)
    return merged


def character_context(characters: tuple[Character, ...], beat: Beat) -> str:
    speakers = {line.speaker for line in beat.dialogue}
    selected = [character for character in characters if character.id in speakers]
    if not selected:
        selected = list(characters)
    return "; ".join(
        f"{item.name} ({item.id}): {item.visual_identity}; wardrobe: {item.wardrobe}"
        for item in selected
    )


def build_prompt(
    episode: Episode,
    scene: Scene,
    beat: Beat,
    duration: int,
    start_state: dict[str, Any],
    end_state: dict[str, Any],
) -> str:
    dialogue = " ".join(f'{line.speaker}: "{line.text}"' for line in beat.dialogue)
    preserve = ", ".join(beat.must_preserve) or "character identity and scene geometry"
    return "\n".join(
        [
            f"Create one continuous {duration}-second animated shot in {episode.visual_style}.",
            f"Frame: {episode.aspect_ratio} at {episode.fps} fps.",
            f"Location: {scene.location}, {scene.time_of_day}. {scene.continuity_anchor}",
            f"Characters: {character_context(episode.characters, beat)}",
            f"Starting state: {start_state}",
            f"Action: {beat.action}",
            f"Dialogue: {dialogue or 'No spoken dialogue.'}",
            f"Camera: {beat.camera}",
            f"Must preserve: {preserve}",
            f"End on this exact state for the next shot: {end_state}",
            (
                "Use readable staging, one primary action, stable designs, "
                "and no cuts within the shot."
            ),
        ]
    )
