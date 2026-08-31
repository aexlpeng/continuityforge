from pathlib import Path

import pytest

from continuityforge.errors import ValidationError
from continuityforge.models import Episode

FIXTURE = Path(__file__).parents[1] / "examples" / "episode-001" / "episode.yaml"


def test_load_example_episode() -> None:
    episode = Episode.load(FIXTURE)
    assert episode.id == "episode-001"
    assert len(episode.characters) == 2
    assert len(episode.scenes[0].beats) == 5


def test_rejects_unknown_speaker() -> None:
    data = {
        "episode": {
            "id": "bad",
            "title": "Bad",
            "logline": "Invalid fixture",
            "visual_style": "original",
        },
        "characters": [
            {"id": "known", "name": "Known", "visual_identity": "round face"}
        ],
        "scenes": [
            {
                "id": "s1",
                "location": "room",
                "continuity_anchor": "one chair",
                "beats": [
                    {
                        "id": "b1",
                        "summary": "test",
                        "action": "waits",
                        "dialogue": [{"speaker": "missing", "text": "hello"}],
                    }
                ],
            }
        ],
    }
    with pytest.raises(ValidationError, match="unknown speaker"):
        Episode.from_dict(data)

