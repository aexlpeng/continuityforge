# Research Plan

## Research question

How much can explicit shot planning, continuity-state propagation, and model routing improve perceived coherence per dollar in one-to-five-minute AI-generated animated stories assembled from 5s/10s shots?

## Hypotheses

- **H1:** Explicit start/end state contracts improve character and prop continuity relative to independent prompts.
- **H2:** Duration-aware planning reduces clipped dialogue and incomplete actions relative to a fixed 5s policy.
- **H3:** Capability-aware routing improves completion rate and cost-adjusted quality relative to a single endpoint.
- **H4:** Repair targeted at the failed continuity field uses less compute than unconditional whole-shot regeneration.

## Experimental units

Use at least three original or permissively licensed episodes. Each episode should contain 12–30 shots and at least three of these stressors: two-character dialogue, repeated location, prop state change, screen text, time jump, entrance/exit, or camera movement.

Run each condition with multiple seeds where endpoints expose seeds. Treat shot generations—not individual frames—as the primary unit, while accounting for episode clustering in analysis.

## Conditions

1. Independent prompts, fixed 5 seconds, single model
2. Independent prompts, fixed 10 seconds, single model
3. Duration-aware planning without state propagation
4. Duration-aware planning plus text state propagation
5. State propagation plus visual reference, when supported
6. Full pipeline with capability/cost routing and bounded repair

## Measures

Primary: blind human ratings for identity consistency, scene/prop continuity, dialogue alignment, motion plausibility, and narrative coherence.

Secondary: completion rate, retry count, latency, estimated cost, identity similarity signal, and state-specific failure labels.

Report distributions and confidence intervals, not only averages. Track inter-rater agreement. Do not use an automatic similarity score as proof of story coherence.

## Deliverables

- Open episode schemas, prompts, configurations, manifests, and aggregate results
- Rights-cleared example outputs where model terms permit
- A reproducible benchmark command and environment lock
- Failure taxonomy and repair-policy ablation
- Technical report describing negative and positive findings

## Compute request rationale

Video ablations multiply quickly across episodes, conditions, seeds, and retries. Grant compute would fund a controlled matrix rather than a single polished demo. The initial study should publish the planned matrix and stop rules before generation to reduce selection bias and uncontrolled spending.

