# Human Evaluator Instructions

Rate each shot from 1 to 5 without seeing the model name or cost.

- Character identity: face, hair, body, clothing, and distinguishing marks remain stable.
- Scene/prop continuity: geometry, lighting, objects, text, and declared state changes are correct.
- Motion plausibility: movement is complete, physically readable, and free of severe artifacts.
- Dialogue alignment: visible speech/reactions fit the line duration and speaker.
- Narrative coherence: the shot communicates its beat and connects to adjacent shots.
- Artifact control: distortions, duplicate elements, text corruption, flicker, and camera errors are limited.

Use 1 for unusable, 2 for major defects, 3 for acceptable with visible issues, 4 for strong with minor issues, and 5 for excellent. Add every applicable failure label and a short evidence-based note. Do not reward style preference under continuity dimensions.

