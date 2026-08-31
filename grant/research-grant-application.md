# fal Research Grant Application Draft

**Project:** ContinuityForge  
**Repository:** https://github.com/aexlpeng/continuityforge  
**Applicant:** [FULL NAME / TEAM]  
**Location:** [CITY, COUNTRY]  
**Contact / fal account email:** [EMAIL]  
**Demo:** [ADD AFTER CREATING A RIGHTS-CLEARED DEMO]  
**License:** Apache-2.0

## One-sentence summary

ContinuityForge is an open-source orchestration and evaluation toolkit for turning 5- and 10-second generative-video shots into coherent one-to-five-minute animated stories with explicit state continuity, duration-aware planning, model routing, and reproducible benchmarks.

## Problem

Short video generations can look excellent in isolation, but assembling them into a story exposes a different class of failures: character identity drifts, wardrobe and props change, locations reset, dialogue exceeds the available motion window, and successful shots are regenerated because provenance is missing. Most creative workflows handle these problems through manual prompt editing, which makes results difficult to reproduce or compare.

The research question is: **how much can explicit shot planning, continuity-state propagation, and capability-aware model routing improve perceived narrative coherence per dollar?**

## Proposed work

The project represents each shot as a transition from a declared start state to a declared end state. A deterministic planner assigns a 5s or 10s window from dialogue load and action complexity. A model router selects a compatible endpoint from configuration. Every request and result is recorded in a manifest, and evaluation separates human continuity judgments from completion, retry, latency, and cost measurements.

With grant support, I will run controlled ablations across at least three original or permissively licensed episodes:

1. Independent prompts with fixed 5s shots
2. Independent prompts with fixed 10s shots
3. Duration-aware planning without state propagation
4. Duration-aware planning plus text state propagation
5. State propagation plus visual reference conditioning where supported
6. Capability/cost routing with bounded repair

Each condition will be evaluated for character identity, scene/prop continuity, motion plausibility, dialogue alignment, narrative coherence, completion rate, retries, latency, and cost. The study will use multiple seeds where supported and at least three blinded raters for publishable human-rating claims.

## Why fal

fal is not only a source of generation credits for this project. Its common model API and queue-backed execution make it possible to benchmark multiple image/video endpoints under one orchestration contract while preserving request IDs and comparable inputs. That shared infrastructure is central to the model-routing and cost/quality experiments.

## Current status

The public v0.1 scaffold includes:

- Typed episode, character, scene, beat, shot, state, and result contracts
- A tested deterministic 5s/10s planner
- Continuity state propagation and prompt compilation
- Configuration-driven model routing
- A fal Python client adapter and no-cost dry-run mode
- Reproducible storyboards, generation manifests, and evaluation sheets
- An original five-shot fixture, prompt templates, benchmark protocol, failure taxonomy, and CI

Live benchmark outputs and a demo video are not yet claimed; those are the next deliverables.

## Open-source deliverables

- Versioned episode fixtures, prompts, model configurations, and manifests
- A reproducible multi-condition benchmark runner
- Aggregate benchmark tables with failures and exclusions included
- State-propagation, duration-policy, routing, and repair ablations
- An openly documented failure taxonomy
- Rights-cleared sample sequences when endpoint and asset terms permit
- A technical report covering both positive and negative results

All pipeline code will remain Apache-2.0. Third-party models and generated media will retain their own terms, and asset provenance will be documented.

## Requested support and compute plan

I am requesting **[REQUESTED CREDIT / COMPUTE AMOUNT]** to execute **[NUMBER] episodes × [NUMBER] conditions × [NUMBER] seeds × [NUMBER] shots**, with a maximum of **[RETRY CAP]** retries per failed shot. Before spending grant credits, I will commit the final experiment matrix, stop rules, endpoint schemas, and verified pricing snapshot.

Planned allocation:

| Work package | Share | Output |
|---|---:|---|
| Baselines and duration-policy ablation | 25% | fixed-window comparison |
| State/reference propagation ablation | 35% | continuity comparison |
| Multi-model routing and repair | 25% | cost/quality frontier |
| Replication, failed-run reserve, final examples | 15% | reproducibility check |

If actual endpoint prices differ from the planning snapshot, I will reduce seeds or conditions transparently rather than exceed the grant.

## Milestones

**Weeks 1–2:** verify fal endpoints, finalize episode fixtures and pre-register benchmark matrix.  
**Weeks 3–5:** implement resumable async runs and produce baseline/duration results.  
**Weeks 6–8:** run state/reference and routing/repair ablations.  
**Weeks 9–10:** blinded evaluation, analysis, documentation, and rights-cleared demo.  
**Weeks 11–12:** replication pass and public technical report.

## Applicant fit

[ADD 100–150 WORDS: relevant engineering, animation, open-source, research, or content-production experience. Link to concrete repositories or shipped work. Do not inflate credentials.]

## Long-term impact

The goal is not another closed animation generator. It is a small, inspectable layer that helps researchers and creators ask better questions of rapidly changing video models: what stayed consistent, what failed, what did the retry cost, and can another person reproduce the result? The same contracts can support satire, education, storyboarding, and other rights-respecting animated formats.
