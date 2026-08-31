from __future__ import annotations

from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any

import yaml

from .errors import ValidationError


def _required(mapping: dict[str, Any], key: str, context: str) -> Any:
    value = mapping.get(key)
    if value is None or value == "":
        raise ValidationError(f"Missing required field '{key}' in {context}")
    return value


@dataclass(frozen=True)
class DialogueLine:
    speaker: str
    text: str

    @classmethod
    def from_dict(cls, data: dict[str, Any], context: str) -> DialogueLine:
        return cls(
            speaker=str(_required(data, "speaker", context)),
            text=str(_required(data, "text", context)),
        )


@dataclass(frozen=True)
class Character:
    id: str
    name: str
    visual_identity: str
    wardrobe: str = ""
    voice: str = ""

    @classmethod
    def from_dict(cls, data: dict[str, Any], context: str) -> Character:
        return cls(
            id=str(_required(data, "id", context)),
            name=str(_required(data, "name", context)),
            visual_identity=str(_required(data, "visual_identity", context)),
            wardrobe=str(data.get("wardrobe", "")),
            voice=str(data.get("voice", "")),
        )


@dataclass(frozen=True)
class Beat:
    id: str
    summary: str
    action: str
    action_complexity: str = "medium"
    dialogue: tuple[DialogueLine, ...] = ()
    camera: str = "medium shot, locked camera"
    must_preserve: tuple[str, ...] = ()
    start_state: dict[str, Any] = field(default_factory=dict)
    end_state: dict[str, Any] = field(default_factory=dict)
    duration_hint: int | None = None
    task: str = "image-to-video"

    @classmethod
    def from_dict(cls, data: dict[str, Any], context: str) -> Beat:
        dialogue = tuple(
            DialogueLine.from_dict(item, f"{context}.dialogue[{index}]")
            for index, item in enumerate(data.get("dialogue", []))
        )
        hint = data.get("duration_hint")
        if hint is not None and hint not in (5, 10):
            raise ValidationError(f"{context}.duration_hint must be 5 or 10")
        complexity = str(data.get("action_complexity", "medium"))
        if complexity not in {"simple", "medium", "complex"}:
            raise ValidationError(
                f"{context}.action_complexity must be simple, medium, or complex"
            )
        return cls(
            id=str(_required(data, "id", context)),
            summary=str(_required(data, "summary", context)),
            action=str(_required(data, "action", context)),
            action_complexity=complexity,
            dialogue=dialogue,
            camera=str(data.get("camera", "medium shot, locked camera")),
            must_preserve=tuple(str(item) for item in data.get("must_preserve", [])),
            start_state=dict(data.get("start_state", {})),
            end_state=dict(data.get("end_state", {})),
            duration_hint=hint,
            task=str(data.get("task", "image-to-video")),
        )


@dataclass(frozen=True)
class Scene:
    id: str
    location: str
    time_of_day: str
    continuity_anchor: str
    initial_state: dict[str, Any]
    beats: tuple[Beat, ...]

    @classmethod
    def from_dict(cls, data: dict[str, Any], context: str) -> Scene:
        beats_data = data.get("beats", [])
        if not beats_data:
            raise ValidationError(f"{context} must contain at least one beat")
        return cls(
            id=str(_required(data, "id", context)),
            location=str(_required(data, "location", context)),
            time_of_day=str(data.get("time_of_day", "unspecified")),
            continuity_anchor=str(_required(data, "continuity_anchor", context)),
            initial_state=dict(data.get("initial_state", {})),
            beats=tuple(
                Beat.from_dict(item, f"{context}.beats[{index}]")
                for index, item in enumerate(beats_data)
            ),
        )


@dataclass(frozen=True)
class Episode:
    id: str
    title: str
    logline: str
    visual_style: str
    aspect_ratio: str
    fps: int
    characters: tuple[Character, ...]
    scenes: tuple[Scene, ...]

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Episode:
        metadata = data.get("episode", {})
        characters_data = data.get("characters", [])
        scenes_data = data.get("scenes", [])
        if not characters_data:
            raise ValidationError("Episode must contain at least one character")
        if not scenes_data:
            raise ValidationError("Episode must contain at least one scene")
        episode = cls(
            id=str(_required(metadata, "id", "episode")),
            title=str(_required(metadata, "title", "episode")),
            logline=str(_required(metadata, "logline", "episode")),
            visual_style=str(_required(metadata, "visual_style", "episode")),
            aspect_ratio=str(metadata.get("aspect_ratio", "16:9")),
            fps=int(metadata.get("fps", 24)),
            characters=tuple(
                Character.from_dict(item, f"characters[{index}]")
                for index, item in enumerate(characters_data)
            ),
            scenes=tuple(
                Scene.from_dict(item, f"scenes[{index}]")
                for index, item in enumerate(scenes_data)
            ),
        )
        episode.validate_references()
        return episode

    def validate_references(self) -> None:
        character_ids = {character.id for character in self.characters}
        if len(character_ids) != len(self.characters):
            raise ValidationError("Character IDs must be unique")
        beat_ids: set[str] = set()
        for scene in self.scenes:
            for beat in scene.beats:
                if beat.id in beat_ids:
                    raise ValidationError(f"Beat ID '{beat.id}' is duplicated")
                beat_ids.add(beat.id)
                for line in beat.dialogue:
                    if line.speaker not in character_ids:
                        raise ValidationError(
                            f"Beat '{beat.id}' references unknown speaker '{line.speaker}'"
                        )

    @classmethod
    def load(cls, path: str | Path) -> Episode:
        source = Path(path)
        with source.open("r", encoding="utf-8") as handle:
            data = yaml.safe_load(handle)
        if not isinstance(data, dict):
            raise ValidationError("Episode file must contain a YAML mapping")
        return cls.from_dict(data)


@dataclass(frozen=True)
class Shot:
    id: str
    episode_id: str
    scene_id: str
    beat_id: str
    index: int
    duration_seconds: int
    task: str
    summary: str
    prompt: str
    negative_prompt: str
    camera: str
    dialogue: tuple[DialogueLine, ...]
    start_state: dict[str, Any]
    end_state: dict[str, Any]
    must_preserve: tuple[str, ...]
    planning_reasons: tuple[str, ...]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

