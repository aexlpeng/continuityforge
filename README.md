# ContinuityForge

**An open-source orchestration and evaluation toolkit for turning short AI-generated video shots into coherent animated stories.**

[![CI](https://github.com/aexlpeng/continuityforge/actions/workflows/ci.yml/badge.svg)](https://github.com/aexlpeng/continuityforge/actions/workflows/ci.yml)
[![License](https://img.shields.io/badge/license-Apache--2.0-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.10%2B-3776AB.svg)](pyproject.toml)
[![fal](https://img.shields.io/badge/inference-fal.ai-ff5c5c.svg)](https://fal.ai)

Today’s video models can generate striking 5- or 10-second clips. Making a one-to-five-minute story is a different problem: characters drift, props jump, locations reset, dialogue overruns shots, and retries become expensive. ContinuityForge treats long-form generation as an orchestration and evaluation problem.

It converts a structured episode into duration-aware shots, carries visual state between shots, routes each shot to a compatible model, records reproducible manifests, and produces an evaluation sheet. The included fal adapter is intentionally thin: model endpoints and arguments stay in configuration rather than being hard-coded.

> **Project status:** early, runnable research scaffold. Planning, validation, dry-run manifests, continuity checks, and evaluation are implemented. Live media generation requires a fal API key and model-specific endpoint configuration. No demo video is included yet.

## Why this project

Single-clip quality is improving quickly, but narrative continuity remains under-measured. ContinuityForge focuses on five testable questions:

1. Can dialogue and action be mapped reliably to discrete 5s/10s generation windows?
2. Which state should pass from one shot to the next to reduce identity and scene drift?
3. When should a failed shot be repaired, regenerated, or routed to another model?
4. How do cost, latency, visual quality, and continuity trade off across models?
5. Can the resulting workflow be reproduced from an episode manifest rather than a pile of prompts?

## What is included

- A typed story, shot, state, generation, and evaluation data model
- A deterministic 5s/10s shot planner based on dialogue load and action complexity
- A continuity engine that creates explicit start/end state contracts
- Configuration-driven model routing with capability and cost metadata
- A queue-backed fal adapter with dry-run mode and no embedded credentials
- Per-shot JSON manifests for provenance and resumability
- Automatic structural checks plus a human evaluation rubric
- Prompt templates for scripts, storyboards, keyframes, video, repair, and judging
- A complete fictional episode specification (without generated media)
- Research Grant and Builder Grant application drafts

## Pipeline

```text
episode.yaml
    │
    ▼
validate story ──► plan 5s/10s shots ──► attach continuity contracts
                                              │
                                              ▼
                                      route model per shot
                                              │
                           ┌──────────────────┴──────────────────┐
                           ▼                                     ▼
                       dry run                         fal queue generation
                           │                                     │
                           └──────────────────┬──────────────────┘
                                              ▼
                                  manifests + evaluation sheet
```

See [Architecture](docs/architecture.md) for design details.

## Quick start

Requirements: Python 3.10 or newer.

```bash
git clone https://github.com/aexlpeng/continuityforge.git
cd continuityforge
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
python -m pip install -e .

# Plan and validate the included episode. No API key or paid call required.
continuityforge plan examples/episode-001/episode.yaml --out runs/episode-001

# Run the orchestration path without calling a model.
continuityforge generate examples/episode-001/episode.yaml \
  --config configs/models.example.yaml \
  --out runs/episode-001 \
  --dry-run

# Create a blank human-scoring sheet.
continuityforge evaluate runs/episode-001/manifest.json \
  --out runs/episode-001/evaluation.json
```

The plan command writes `storyboard.json`; generate writes `manifest.json`. Both are deterministic for the same inputs.

## Live fal generation

Install the optional client, set the key server-side, and replace the illustrative endpoint IDs/argument templates in the model configuration with endpoints whose current schemas you have verified in the fal model gallery.

```bash
python -m pip install -e ".[fal]"
export FAL_KEY="your-key"  # PowerShell: $env:FAL_KEY="your-key"

continuityforge generate examples/episode-001/episode.yaml \
  --config configs/models.example.yaml \
  --out runs/episode-001
```

ContinuityForge uses the official Python client's queue-backed `subscribe()` method. It does not download returned media automatically in this scaffold; it records the complete provider response in the run manifest so storage policy can be chosen by the operator.

Never commit `FAL_KEY`, generated media containing private inputs, or provider responses that contain sensitive URLs.

## Repository map

```text
continuityforge/
├── src/continuityforge/      # planner, continuity, routing, fal adapter, CLI
├── tests/                    # unit and integration-style dry-run tests
├── configs/                  # model routing example
├── examples/episode-001/     # story, character bible, expected storyboard
├── prompts/                  # reusable prompt contracts
├── evaluation/               # rubric and benchmark protocol
├── docs/                     # architecture, research plan, fal integration
└── grant/                    # ready-to-edit grant application drafts
```

## Evaluation

The benchmark separates **automatic checks** (duration, missing state, required prompt fields, completion rate) from **human judgments** (character, scene, motion, dialogue, narrative, and artifact quality). This prevents a single opaque “quality score” from hiding failure modes.

Recommended reporting unit:

| Metric | Unit | Better |
|---|---:|---:|
| Character identity consistency | 1–5 MOS | higher |
| Scene/prop continuity | 1–5 MOS | higher |
| Motion plausibility | 1–5 MOS | higher |
| Narrative coherence | 1–5 MOS | higher |
| Successful shots | % | higher |
| Regenerations | count/shot | lower |
| End-to-end latency | seconds | lower |
| Estimated generation cost | USD/minute | lower |

See the [evaluation protocol](evaluation/benchmark_protocol.md) and [scorecard](evaluation/scorecard.md).

## Research outputs

The project is designed to publish:

- Versioned episode specifications and shot manifests
- Model/configuration matrices without secrets
- Aggregate benchmark results and failure taxonomy
- Ablations for state propagation, duration policy, and routing strategy
- Reproducible prompt templates and evaluation instructions

Generated media will only be published when rights and model terms permit it.

## Roadmap

The first milestone is a trustworthy benchmarkable orchestrator, not a full editor. Next milestones add resumable async execution, reference-image handling, repair policies, automatic similarity signals, and timeline export. See [ROADMAP.md](ROADMAP.md).

## Grant fit

ContinuityForge has two honest application paths:

- **fal Research Grant:** best fit now. The repository is open source and proposes reproducible research on multi-shot consistency, routing, and cost/quality tradeoffs.
- **fal Builder Grant:** suitable once a direct user-facing generative-media product or hosted workflow exists. The current fal page states that this program is for direct generative-media apps and that applications are currently routed through approved partners.

Application drafts are in [`grant/`](grant/). Replace all bracketed fields and attach a real demo before submission.

## Contributing

Contributions are welcome, especially new provider adapters, endpoint configurations, continuity metrics, and openly licensed episode fixtures. Read [CONTRIBUTING.md](CONTRIBUTING.md) and the [Code of Conduct](CODE_OF_CONDUCT.md).

## Responsible use

This repository is infrastructure, not permission to imitate a living artist, clone a person's identity or voice, or use protected media without rights. Contributors must document asset provenance and follow endpoint terms and applicable law. See [SECURITY.md](SECURITY.md) for vulnerability reporting and secret-handling guidance.

## License

Apache License 2.0. See [LICENSE](LICENSE). Model weights, generated outputs, and third-party assets remain subject to their own licenses and terms.
