from pathlib import Path

import pytest

from continuityforge.errors import PlanningError
from continuityforge.models import Beat, DialogueLine, Episode
from continuityforge.planner import choose_duration, count_words, plan_episode

FIXTURE = Path(__file__).parents[1] / "examples" / "episode-001" / "episode.yaml"


def test_word_count_supports_english_and_cjk() -> None:
    assert count_words("Two clear words") == 3
    assert count_words("你好 AI") == 3


def test_short_action_uses_five_seconds() -> None:
    beat = Beat(id="b", summary="s", action="blinks", action_complexity="simple")
    assert choose_duration(beat)[0] == 5


def test_oversized_beat_requires_split() -> None:
    beat = Beat(
        id="b",
        summary="s",
        action="talks",
        action_complexity="complex",
        dialogue=(DialogueLine(speaker="narrator", text="one " * 30),),
    )
    with pytest.raises(PlanningError, match="Split it"):
        choose_duration(beat)


def test_plan_propagates_end_state() -> None:
    shots = plan_episode(Episode.load(FIXTURE))
    assert [shot.duration_seconds for shot in shots] == [5, 10, 10, 5, 10]
    assert shots[1].start_state["meeting_screen"] == "glowing blue with text DAILY STAND-UP"
    assert shots[-1].start_state["wall_clock"] == "18:30"
