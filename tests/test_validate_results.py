
import json
import unittest

from scripts.validate_results import DEFAULT_SCHEMA, validate_history


def load_schema():
    return json.loads(DEFAULT_SCHEMA.read_text(encoding="utf-8"))


class ValidateHistoryTests(unittest.TestCase):

    def setUp(self):
        self.schema = load_schema()

    def test_empty_history_is_valid(self):
        self.assertEqual(
            validate_history(
                {"schema_version": 1, "results": []},
                self.schema,
            ),
            [],
        )

    def test_valid_result_is_accepted(self):
        history = {
            "schema_version": 1,
            "results": [
                {
                    "client_version": "2026.1.0",
                    "platform": "linux",
                    "vaultwarden_version": "1.34.0",
                    "result": "pass",
                    "tested_at": "2026-11-20T09:00:00Z",
                    "test_suite_revision": "abc123",
                }
            ],
        }

        self.assertEqual(
            validate_history(history, self.schema),
            [],
        )

    def test_unknown_platform_is_rejected(self):
        history = {
            "schema_version": 1,
            "results": [
                {
                    "client_version": "2026.1.0",
                    "platform": "macos",
                    "vaultwarden_version": "1.34.0",
                    "result": "pass",
                    "tested_at": "2026-11-20T09:00:00Z",
                    "test_suite_revision": "abc123",
                }
            ],
        }

        errors = validate_history(history, self.schema)

        self.assertTrue(
            any("platform" in error for error in errors)
        )

    def test_invalid_timestamp_is_rejected(self):
        history = {
            "schema_version": 1,
            "results": [
                {
                    "client_version": "2026.1.0",
                    "platform": "linux",
                    "vaultwarden_version": "1.34.0",
                    "result": "pass",
                    "tested_at": "not-a-timestamp",
                    "test_suite_revision": "abc123",
                }
            ],
        }

        errors = validate_history(history, self.schema)

        self.assertTrue(
            any("date-time" in error for error in errors)
        )

    def test_missing_required_field_is_rejected(self):
        history = {
            "schema_version": 1,
            "results": [
                {"client_version": "2026.1.0"}
            ],
        }

        errors = validate_history(history, self.schema)

        self.assertTrue(
            any("required" in error for error in errors)
        )

    def test_invalid_history_envelope_is_rejected(self):
        self.assertTrue(
            validate_history([], self.schema)
        )

        self.assertTrue(
            any(
                "schema_version" in error
                for error in validate_history(
                    {"schema_version": 2, "results": []},
                    self.schema,
                )
            )
        )

        self.assertTrue(
            any(
                "must be an array" in error
                for error in validate_history(
                    {"schema_version": 1, "results": {}},
                    self.schema,
                )
            )
        )

        self.assertTrue(
            any(
                "schema_version" in error
                for error in validate_history(
                    {"schema_version": True, "results": []},
                    self.schema,
                )
            )
        )


if __name__ == "__main__":
    unittest.main()
