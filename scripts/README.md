
# Scripts

## Result validation

`validate_results.py` validates `registry/history.json` against
`compatibility/results.schema.json`, including JSON Schema date-time
format checks.

It exits non-zero for:

- Malformed JSON.
- An invalid history envelope.
- An invalid JSON Schema.
- Results that violate the result contract.

Install development dependencies:

```bash
python -m pip install -r requirements-dev.txt
```

Run validation:

```bash
python scripts/validate_results.py
```

Release discovery, compatibility-matrix selection, and registry/README
generation remain future work.

Scripts that alter a user's installed update configuration will be
added only after the official updater mechanism for that platform
has been verified and documented.
