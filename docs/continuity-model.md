# Continuity Model

## The problem

A multi-shot sequence fails when a later shot contradicts a fact established earlier: identity, wardrobe, handedness, object location, lighting direction, pose, gaze, screen content, or scene geometry. Prompt repetition helps, but it does not say which facts changed intentionally.

ContinuityForge represents each shot as a state transition:

```text
S(start) + action + camera intent → S(end)
```

The next shot inherits `S(end)` unless its beat explicitly overrides a field. This makes intentional changes reviewable. For example, changing `blue_mug: full` to `blue_mug: empty` is a declared story event; an unrequested color change remains a failure.

## State-writing guidelines

- Record visually observable facts, not internal emotions.
- Use stable nouns: `blue_mug`, not `it`.
- Express positions relative to persistent anchors.
- Keep character identity in the character bible; state holds the current pose/placement.
- Put only changes in `end_state`; inherited fields remain in force.
- Treat on-screen text as a state field because video models often corrupt it.

## Hard locks and soft intent

`must_preserve` is a hard lock for evaluation and repair. Camera and action are soft intent: minor deviations may be acceptable when identity and narrative beats survive.

## Future visual propagation

Text state alone cannot guarantee pixel continuity. Planned adapters will add:

- First-frame generation from a locked character/location reference
- Last-frame extraction and next-shot conditioning
- Masked correction for props or faces
- Reference-strength sweeps
- Identity and scene embedding signals for triage

These techniques should be evaluated as separate ablations so improvements are attributable.

