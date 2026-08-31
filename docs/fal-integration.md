# fal Integration

## Why fal is useful here

ContinuityForge needs to run the same structured story against multiple generative-media endpoints while preserving manifests, queue reliability, and comparable inputs. fal's model APIs provide a common client surface for image/video models, which makes model routing and controlled benchmarking practical.

## Authentication

Create an API-scoped key in the fal dashboard and expose it as `FAL_KEY` only in the server-side environment. The official Python client reads that variable automatically. Do not place a key in YAML, source code, a notebook, or a client-side app.

## Endpoint configuration

Model endpoint IDs and input schemas are not assumed to be stable. Before a live run:

1. Select a current endpoint in the fal model gallery.
2. Copy its exact endpoint ID into `configs/models.example.yaml` or a private derived config.
3. Map that endpoint's required fields under `arguments`.
4. Confirm supported duration values and reference-image requirements.
5. Record pricing and the date it was verified in the benchmark run notes.
6. Execute one dry run and inspect every rendered argument.

Template tokens currently supported are `{prompt}`, `{negative_prompt}`, `{duration_seconds}`, and `{shot_id}`.

## Queue behavior

The live adapter uses `fal_client.subscribe()`, which is queue-backed and blocks while polling. It captures the request ID through `on_enqueue`. For larger studies, replace this with `submit()`/webhooks and a persistent job store so runs can resume after worker failure.

## Retention and privacy

Provider payload and media-retention behavior can change. Verify current fal documentation before processing private assets. A production implementation may pass platform headers for stricter retention, but those choices are intentionally not hard-coded because they are policy decisions and must be tested against the current API.

## Cost controls

- Default to dry-run.
- Require explicit live mode; there is no implicit fallback from dry-run.
- Validate every endpoint and shot duration before the first paid call.
- Start with one episode and one model.
- Persist request IDs and do not regenerate successful shots.
- Define a retry budget and stop on systematic validation failures.
- Snapshot per-model pricing for each benchmark report.

## Current limitation

The example model IDs are placeholders so the repository cannot accidentally spend credits against an outdated or unintended endpoint. A real demo PR should add a verified configuration plus a dated note, while keeping the key secret.

