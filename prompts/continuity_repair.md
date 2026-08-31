# Continuity Repair Contract

Repair a generated shot using a failed-field report.

## Inputs

- Approved first frame/reference
- Generated candidate
- Start/end state contract
- Exact failed fields
- Elements that already passed

## Rules

Change only what is required to fix the failed fields. Preserve timing, camera, identities, props, and successful regions. Do not “improve” the style or introduce detail not present in the reference. If repair would alter more than one-third of the shot or the narrative action is missing, recommend regeneration instead.

Return: `decision` (`repair` or `regenerate`), `reason`, `repair_prompt`, and the constraints that must remain locked.

