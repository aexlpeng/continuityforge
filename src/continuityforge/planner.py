from __future__ import annotations

import re

from .continuity import DEFAULT_NEGATIVE_PROMPT, build_prompt, merge_state
from .errors import PlanningError
from .models import Beat, Episode, Shot

SPEAKING_WORDS_PER_SECOND = 2.5
ACTION_SECONDS = {"simple": 1.5, "medium": 3.0, "complex": 5.0}


def count_words(text: str) -> int:
    """Count Latin words and CJK characters conservatively for timing."""
    latin = re.findall(r"[A-Za-z0-9']+", text)
    cjk = re.findall(r"[\u3400-\u9fff]", text)
    return len(latin) + len(cjk)


def choose_duration(beat: Beat) -> tuple[int, tuple[str, ...]]:
    if beat.duration_hint:
        return beat.duration_hint, (f"author duration_hint={beat.duration_hint}",)

    word_count = sum(count_words(line.text) for line in beat.dialogue)
    speech_seconds = word_count / SPEAKING_WORDS_PER_SECOND
    action_seconds = ACTION_SECONDS[beat.action_complexity]
    estimated = max(action_seconds, speech_seconds + 1.0 if word_count else action_seconds)
    reasons = (
        f"dialogue_words={word_count}",
        f"speech_estimate={speech_seconds:.1f}s",
        f"dialogue_lines={len(beat.dialogue)}",
        f"action_complexity={beat.action_complexity}",
        f"total_estimate={estimated:.1f}s",
    )
    if len(beat.dialogue) >= 2 and estimated <= 10:
        return 10, reasons + ("two-speaker/reaction pacing requires the 10s window",)
    if estimated <= 5:
        return 5, reasons
    if estimated <= 10:
        return 10, reasons
    raise PlanningError(
        f"Beat '{beat.id}' is estimated at {estimated:.1f}s. Split it into smaller beats; "
        "a single generation shot cannot exceed 10 seconds."
    )


def plan_episode(episode: Episode) -> list[Shot]:
    shots: list[Shot] = []
    previous_end_state: dict[str, object] = {}
    shot_index = 1

    for scene in episode.scenes:
        scene_state = merge_state(previous_end_state, scene.initial_state)
        for beat in scene.beats:
            duration, reasons = choose_duration(beat)
            start_state = merge_state(scene_state, beat.start_state)
            end_state = merge_state(start_state, beat.end_state)
            shot_id = f"shot-{shot_index:03d}"
            shots.append(
                Shot(
                    id=shot_id,
                    episode_id=episode.id,
                    scene_id=scene.id,
                    beat_id=beat.id,
                    index=shot_index,
                    duration_seconds=duration,
                    task=beat.task,
                    summary=beat.summary,
                    prompt=build_prompt(
                        episode, scene, beat, duration, start_state, end_state
                    ),
                    negative_prompt=DEFAULT_NEGATIVE_PROMPT,
                    camera=beat.camera,
                    dialogue=beat.dialogue,
                    start_state=start_state,
                    end_state=end_state,
                    must_preserve=beat.must_preserve,
                    planning_reasons=reasons,
                )
            )
            scene_state = end_state
            previous_end_state = end_state
            shot_index += 1
    return shots
