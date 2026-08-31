# Contributing to ContinuityForge

Thank you for helping make multi-shot generative video more reproducible.

## Good first contributions

- Add an openly licensed episode fixture that exposes a specific continuity problem.
- Add or verify a model configuration without committing credentials.
- Improve a metric, report template, or failure label.
- Add a provider adapter behind the existing `GenerationClient` contract.
- Reproduce a benchmark and report both successful and failed shots.

## Development setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
python -m pip install -e ".[dev]"
pytest
ruff check .
```

## Pull requests

Keep pull requests focused. Describe the problem, the change, how it was tested, and any model/API cost incurred. If results depend on a model, record the endpoint, configuration, date, seed when available, and number of retries. Do not commit API keys or private media URLs.

Code changes should include tests. Documentation and benchmark contributions should state asset provenance and known limitations. By contributing, you agree that your contribution is licensed under Apache-2.0.

## Benchmark integrity

Do not remove failed generations from aggregate results without reporting the exclusion rule. Separate human ratings from automatic metrics, preserve raw per-shot scores, and avoid claiming statistical significance without enough independent samples.

