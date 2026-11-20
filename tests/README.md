
# Compatibility tests

Platform-specific end-to-end tests will live here.

The first implementation step establishes validation of persisted
compatibility results before any automated workflow is allowed
to consume or publish them.

Run the validation unit tests from the repository root:

```bash
python -m pip install -r requirements-dev.txt
python -m unittest discover -s tests -v
```

Validate the current registry history:

```bash
python scripts/validate_results.py
```

Never use personal Bitwarden accounts, real vault data,
or production credentials in CI.
