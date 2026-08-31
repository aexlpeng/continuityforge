# Security Policy

## Supported versions

Until version 1.0, security fixes are applied to the latest release and the default branch.

## Reporting a vulnerability

Do not open a public issue for credential exposure, arbitrary file access, unsafe URL handling, or another exploitable flaw. Contact the repository owner through the private contact method on their GitHub profile and include reproduction steps, impact, and a suggested fix if available.

## Secrets and generated assets

- Store `FAL_KEY` only in the environment or a secret manager.
- Never place keys in episode files, prompts, model configuration, logs, or manifests.
- Treat model response URLs as potentially sensitive and short-lived.
- Review provider data-retention controls before sending confidential inputs.
- Do not automatically download or execute arbitrary URLs from model output.
- Keep generated media out of Git unless its license, provenance, and consent are documented.

