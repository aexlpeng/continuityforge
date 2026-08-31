# Benchmark Protocol

## Pre-register the run

Before generating media, commit the episode set, endpoint configuration, conditions, number of seeds, maximum retries, exclusion rules, and evaluation plan. Record current endpoint schemas and prices with a verification date.

## Generation

1. Run `plan` and review shot contracts before any paid request.
2. Run `generate --dry-run` and inspect rendered arguments.
3. Execute conditions in randomized episode/seed order when practical.
4. Preserve every request ID, result, error, latency, and retry.
5. Do not cherry-pick the best seed without reporting the selection budget.
6. Assemble sequences with identical transition/audio rules across conditions.

## Evaluation

- Use at least three independent raters for claims intended for publication.
- Blind raters to model/condition and randomize sequence order.
- Collect per-shot ratings before overall episode coherence.
- Report agreement and raw sample counts.
- Separate blocked/provider failures from visual-quality failures, but include both in completion rate.

## Reporting

Publish mean, median, dispersion, confidence intervals where justified, total shots, failures, retries, compute cost, and latency. Include negative results. Identify any media withheld for license, consent, safety, or provider-term reasons.

## Minimum reproducibility bundle

- Git commit SHA and Python version
- Episode YAML and character bible
- Model config with no secret
- Storyboard and run manifest
- Evaluator instructions and anonymized raw ratings
- Aggregation script or notebook
- Asset provenance statement

