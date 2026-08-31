# Script Writer Contract

Write an original 60–300 second animated story designed for 5s/10s generative-video shots.

## Inputs

- Audience, theme, tone, target duration
- Original character identities and location constraints
- Required narrative stressors for evaluation

## Requirements

1. Use only original characters and dialogue; do not imitate a named living artist or existing franchise.
2. Give each beat one primary visible action and no more than two short dialogue lines.
3. Make every beat independently filmable in either 5 or 10 seconds.
4. Introduce persistent visual anchors in the first beat of each location.
5. Declare intentional state changes: pose, prop location, screen content, lighting, entrances/exits.
6. End on a visually legible state that can seed the next shot.
7. If a beat needs more than 10 seconds, split it before output.

## Output

Return YAML matching `examples/episode-001/episode.yaml`. Do not add prose around the YAML. Stable IDs must be lowercase kebab-case. Every dialogue speaker must match a character ID.

