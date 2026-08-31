# Failure Taxonomy

## Identity

Face or body structure changes, distinguishing marks disappear, wardrobe mutates, or two characters blend. Diagnose per character and per transition.

## State

A prop appears/disappears, occupies the wrong position, changes state unintentionally, or an entrance/exit is contradicted. Compare against explicit state fields, not memory alone.

## Scene

Geometry, lighting direction, background anchors, time of day, or screen text resets. Some style drift is acceptable if spatial facts remain readable.

## Temporal action

The action starts but does not complete, repeats unnaturally, accelerates to fit, or ends on the wrong pose. This often indicates a duration-planning failure rather than a model-quality failure.

## Camera

Unexpected cuts, zooms, angle flips, lens changes, or subject cropping. Distinguish model-generated motion from an intentionally specified camera move.

## Provider/system

Validation error, policy block, timeout, queue failure, unavailable endpoint, corrupt response, or missing media. Retain these in completion metrics.

## Repair decision

- **Accept:** no material story or continuity failure.
- **Repair:** localized defect; most pixels/timing are correct.
- **Regenerate:** identity, action, camera, or more than one-third of the shot is wrong.
- **Rewrite/replan:** repeated failure indicates the prompt or beat is infeasible.
- **Reroute:** endpoint capability is mismatched to the shot.

