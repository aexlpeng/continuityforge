# Storyboard Planner Contract

Convert an episode specification into a shot list without changing its story.

For each beat:

- Choose 5s for a simple action or one short line.
- Choose 10s for two short lines, complex movement, or a necessary reaction hold.
- Reject and split beats that cannot finish within 10s.
- Carry the previous end state into the next start state.
- State the camera framing and one motivated movement at most.
- List hard continuity locks separately from aesthetic preferences.
- Specify a final pose/composition usable as the next shot's reference.

Return structured data only. Do not invent new props, wardrobe, background characters, dialogue, or cuts within a shot.

