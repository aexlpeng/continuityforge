# Roadmap

The roadmap is outcome-based. Dates depend on maintainer capacity and compute access.

## Milestone 0 — Reproducible scaffold (current)

- [x] Typed episode and shot contracts
- [x] Deterministic 5s/10s planning
- [x] Explicit continuity state propagation
- [x] Config-driven model routing
- [x] fal queue adapter and no-cost dry-run mode
- [x] Generation manifests and evaluation sheets
- [x] Example episode, prompt suite, documentation, and tests

## Milestone 1 — First open benchmark

- [ ] Generate at least three licensed episodes across two or more video endpoints
- [ ] Publish aggregate cost, latency, completion, and human-rating results
- [ ] Add resumable asynchronous execution and bounded repair retries
- [ ] Version endpoint schemas and capture provider request IDs
- [ ] Release a failure taxonomy with representative, rights-cleared frames

## Milestone 2 — Continuity experiments

- [ ] Reference-image and last-frame conditioning adapters
- [ ] State propagation ablation: none vs text state vs visual reference
- [ ] Duration-policy ablation: fixed 5s vs fixed 10s vs planned
- [ ] Character and scene embedding signals as assistive metrics
- [ ] Multi-rater evaluation with agreement reporting

## Milestone 3 — Production bridge

- [ ] Repair/regenerate/reroute policy engine
- [ ] Timeline export for common non-linear editors
- [ ] Optional asset store with checksums and provenance
- [ ] Webhook-based worker example and observability dashboard
- [ ] Hosted, direct generative-media workflow suitable for Builder Grant validation

## Non-goals for the current release

- Training a foundation video model
- Providing a full non-linear video editor
- Claiming cross-model comparability without controlled prompts and raters
- Shipping a demo video before the generation and asset rights are verified

