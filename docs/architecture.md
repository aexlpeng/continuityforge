# Architecture

ContinuityForge separates narrative intent, orchestration, provider calls, and evaluation so each can change independently.

## Design principles

1. **Structured intent before prompts.** Episode YAML is the source of truth; prompts are compiled artifacts.
2. **State is explicit.** Each shot has a start-state and end-state contract that can be inspected and scored.
3. **Provider details live in configuration.** Endpoint IDs and request fields change faster than story logic.
4. **Dry-run is first class.** Planning and routing must be testable without paid inference.
5. **Failures are data.** Manifests retain every attempt; benchmarks report completion and retry counts.
6. **Automatic metrics assist human judgment.** They do not substitute for narrative evaluation.

## Components

### Episode model

`models.py` parses a human-editable YAML file into characters, scenes, beats, dialogue, and state declarations. Validation rejects duplicate beats, unknown dialogue speakers, unsupported duration hints, and malformed action complexity.

### Shot planner

`planner.py` estimates the time needed for speech and action, then assigns a supported 5s or 10s window. A beat estimated above 10 seconds fails with an instruction to split it. Silent shots are driven by action complexity; spoken shots reserve one second for reaction/breathing room.

This policy is deliberately legible rather than “smart.” It creates a baseline that later learned or language-model planners can beat in controlled experiments.

### Continuity engine

`continuity.py` merges state in this order:

```text
previous shot end state
  < scene initial state
  < beat start-state overrides
  < beat end-state updates
```

The merged state is compiled into the prompt together with character identity locks, camera intent, required preserved elements, and an exact end-state target. A future reference-image adapter can use the same contract without changing the story schema.

### Model router

`router.py` filters models by task and supported duration. It chooses the lowest numerical priority and then the lowest declared cost. Costs are optional because model pricing changes; benchmark runs should snapshot verified values rather than relying on this example file.

### Generation adapter

`generation.py` defines a minimal provider contract. `DryRunClient` renders request arguments without making a network call. `FalClient` uses queue-backed `fal_client.subscribe`, captures the provider request ID when available, and stores the raw JSON response in the manifest.

The scaffold stops at response capture. Download policy, URL allowlisting, checksums, durable storage, and media assembly must be implemented explicitly rather than hidden in a convenience function.

### Evaluation

`evaluator.py` records machine-checkable structure and creates empty human rating rows. The benchmark protocol requires raw shot ratings, a failure taxonomy, cost, latency, retries, and exclusions.

## Data contracts

### Episode input

The YAML source controls creative intent. Its stable identifiers (`episode`, `scene`, `beat`, `character`) make results comparable across model runs.

### Storyboard output

`storyboard.json` contains fully compiled shots before model routing. It is suitable for review and diffing.

### Run manifest

`manifest.json` joins each shot with the chosen model configuration and generation result. It is the provenance record for evaluation and resume logic.

### Evaluation sheet

`evaluation.json` pairs automatic checks with one blank rating row per shot. Multiple independent copies should be collected for multiple raters and aggregated separately.

## Extension points

- New planner: accept `Episode`, return ordered `Shot` objects.
- New provider: implement `GenerationClient.generate(model, shot)`.
- New router: preserve compatibility checks and record the selection reason.
- New evaluator: append metrics; do not silently replace raw scores.
- New media store: verify URL scheme/host, stream with limits, hash bytes, and record provenance.

## Threat boundaries

Episode files, prompt outputs, provider responses, and media URLs are untrusted inputs. They must never become shell commands. API keys remain outside manifests. A production worker should use outbound URL allowlists, size/time limits, content review, and isolated media tooling.

