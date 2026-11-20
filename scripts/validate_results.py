
#!/usr/bin/env python3
"""Validate registry/history.json against the project's result contract."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator, FormatChecker
from jsonschema.exceptions import SchemaError


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_HISTORY = ROOT / "registry" / "history.json"
DEFAULT_SCHEMA = ROOT / "compatibility" / "results.schema.json"


class ValidationFailure(Exception):
    """Raised when a registry document is structurally or semantically invalid."""


def load_json(path: Path) -> Any:
    try:
        with path.open("r", encoding="utf-8") as file:
            return json.load(file)
    except OSError as exc:
        raise ValidationFailure(f"cannot read {path}: {exc}") from exc
    except json.JSONDecodeError as exc:
        raise ValidationFailure(
            f"invalid JSON in {path} at line {exc.lineno}, "
            f"column {exc.colno}: {exc.msg}"
        ) from exc


def validate_history(history: Any, schema: Any) -> list[str]:
    """Return human-readable validation errors; an empty list means valid."""
    errors: list[str] = []

    try:
        Draft202012Validator.check_schema(schema)
    except SchemaError as exc:
        return [f"result schema is invalid: {exc.message}"]

    if not isinstance(history, dict):
        return ["history must be a JSON object"]

    if type(history.get("schema_version")) is not int or history["schema_version"] != 1:
        errors.append("history.schema_version must be 1")

    results = history.get("results")
    if not isinstance(results, list):
        errors.append("history.results must be an array")
        return errors

    validator = Draft202012Validator(
        schema,
        format_checker=FormatChecker(),
    )

    for index, result in enumerate(results):
        for error in validator.iter_errors(result):
            location = ".".join(str(part) for part in error.absolute_path)
            prefix = f"history.results[{index}]"

            if location:
                prefix += f".{location}"

            errors.append(f"{prefix}: {error.message}")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Validate registry/history.json against "
            "the compatibility result schema."
        )
    )

    parser.add_argument("--history", type=Path, default=DEFAULT_HISTORY)
    parser.add_argument("--schema", type=Path, default=DEFAULT_SCHEMA)

    args = parser.parse_args()

    try:
        history = load_json(args.history)
        schema = load_json(args.schema)
        errors = validate_history(history, schema)

    except ValidationFailure as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2

    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)

        print(
            f"Validation failed with {len(errors)} error(s).",
            file=sys.stderr,
        )
        return 1

    result_count = len(history["results"])

    print(
        f"Validation successful: {result_count} compatibility result(s)."
    )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
