
# Compatibility tests

Platform-specific end-to-end tests will live here.

The first implementation step establishes validation of persisted
compatibility results and synthetic vault import fixtures before
automated workflows are allowed to consume or publish them.

## Setup

Install the locked development dependencies from the repository root:

```bash
uv sync --locked
```

## Run tests

Run all unit tests:

```bash
uv run python -m unittest discover -s tests -v
```

Validate the current registry history:

```bash
uv run python scripts/validate_results.py
```

The synthetic Bitwarden vault import fixture is located at:

```text
tests/fixtures/vault-canary.json
```

Its structure is validated by:

```text
tests/test_validate_canary_fixture.py
```

Never use personal Bitwarden accounts, real vault data,
or production credentials in CI.
