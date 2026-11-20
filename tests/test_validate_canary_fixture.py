
import json
import unittest
import uuid
from pathlib import Path


FIXTURE_PATH = (
    Path(__file__).parent
    / "fixtures"
    / "vault-canary.json"
)

EXPECTED_ITEM_TYPES = {
    1: "login",
    2: "secureNote",
    3: "card",
    4: "identity",
}

EXPECTED_ITEM_NAMES = {
    "Canary Login",
    "Canary Secure Note",
    "Canary Payment Card",
    "Canary Identity",
}


def load_fixture():
    with FIXTURE_PATH.open(encoding="utf-8") as fixture_file:
        return json.load(fixture_file)


def is_uuid(value):
    if not isinstance(value, str):
        return False

    try:
        uuid.UUID(value)
    except ValueError:
        return False

    return True


class CanaryFixtureTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.fixture = load_fixture()

    def test_fixture_has_expected_top_level_structure(self):
        self.assertEqual(
            set(self.fixture.keys()),
            {"folders", "items"},
        )

        self.assertIsInstance(self.fixture["folders"], list)
        self.assertIsInstance(self.fixture["items"], list)

    def test_fixture_contains_one_folder(self):
        folders = self.fixture["folders"]

        self.assertEqual(len(folders), 1)

        folder = folders[0]

        self.assertEqual(
            folder["name"],
            "Compatibility Test Folder",
        )
        self.assertTrue(is_uuid(folder["id"]))

    def test_fixture_contains_all_expected_item_types(self):
        items = self.fixture["items"]

        self.assertEqual(len(items), 4)

        actual_types = {
            item["type"]
            for item in items
        }

        self.assertEqual(
            actual_types,
            set(EXPECTED_ITEM_TYPES),
        )

    def test_item_names_are_unique_and_expected(self):
        names = [
            item["name"]
            for item in self.fixture["items"]
        ]

        self.assertEqual(len(names), len(set(names)))
        self.assertEqual(set(names), EXPECTED_ITEM_NAMES)

    def test_all_item_ids_are_valid_and_unique(self):
        item_ids = [
            item["id"]
            for item in self.fixture["items"]
        ]

        self.assertEqual(len(item_ids), len(set(item_ids)))

        for item_id in item_ids:
            self.assertTrue(
                is_uuid(item_id),
                f"Invalid item UUID: {item_id}",
            )

    def test_folder_ids_are_valid_and_unique(self):
        folder_ids = [
            folder["id"]
            for folder in self.fixture["folders"]
        ]

        self.assertEqual(len(folder_ids), len(set(folder_ids)))

        for folder_id in folder_ids:
            self.assertTrue(
                is_uuid(folder_id),
                f"Invalid folder UUID: {folder_id}",
            )

    def test_items_reference_existing_folders(self):
        folder_ids = {
            folder["id"]
            for folder in self.fixture["folders"]
        }

        for item in self.fixture["items"]:
            with self.subTest(item=item["name"]):
                self.assertIn(
                    item["folderId"],
                    folder_ids,
                )

    def test_items_use_individual_vault_format(self):
        for item in self.fixture["items"]:
            with self.subTest(item=item["name"]):
                self.assertIsNone(item["organizationId"])

                # Bitwarden's individual-vault JSON format
                # uses null for collectionIds.
                self.assertIsNone(item["collectionIds"])

    def test_each_item_has_its_required_type_specific_object(self):
        for item in self.fixture["items"]:
            expected_object = EXPECTED_ITEM_TYPES[item["type"]]

            with self.subTest(item=item["name"]):
                self.assertIn(expected_object, item)
                self.assertIsInstance(item[expected_object], dict)

    def test_items_have_common_required_fields(self):
        required_fields = {
            "id",
            "organizationId",
            "folderId",
            "type",
            "name",
            "notes",
            "favorite",
            "fields",
            "collectionIds",
        }

        for item in self.fixture["items"]:
            with self.subTest(item=item["name"]):
                self.assertTrue(
                    required_fields.issubset(item.keys())
                )

                self.assertIsInstance(item["name"], str)
                self.assertIsInstance(item["notes"], str)
                self.assertIsInstance(item["favorite"], bool)
                self.assertIsInstance(item["fields"], list)

    def test_custom_fields_have_valid_structure_and_types(self):
        valid_field_types = {0, 1, 2, 3}

        for item in self.fixture["items"]:
            for field in item["fields"]:
                with self.subTest(
                    item=item["name"],
                    field=field.get("name"),
                ):
                    self.assertIsInstance(field.get("name"), str)
                    self.assertIsInstance(field.get("value"), str)
                    self.assertIn(
                        field.get("type"),
                        valid_field_types,
                    )

    def test_login_contains_expected_data(self):
        login = next(
            item["login"]
            for item in self.fixture["items"]
            if item["type"] == 1
        )

        self.assertEqual(login["username"], "canary-user")
        self.assertTrue(login["password"])
        self.assertTrue(login["totp"])

        self.assertIsInstance(login["uris"], list)
        self.assertGreaterEqual(len(login["uris"]), 1)

        for uri in login["uris"]:
            self.assertIsNone(uri["match"])
            self.assertTrue(uri["uri"].startswith("https://"))

    def test_secure_note_contains_multiline_notes(self):
        item = next(
            item
            for item in self.fixture["items"]
            if item["type"] == 2
        )

        self.assertEqual(item["secureNote"]["type"], 0)
        self.assertGreaterEqual(item["notes"].count("\n"), 2)

    def test_card_contains_expected_fields(self):
        card = next(
            item["card"]
            for item in self.fixture["items"]
            if item["type"] == 3
        )

        required_fields = {
            "cardholderName",
            "brand",
            "number",
            "expMonth",
            "expYear",
            "code",
        }

        self.assertTrue(
            required_fields.issubset(card.keys())
        )

        for field in required_fields:
            self.assertIsInstance(card[field], str)
            self.assertTrue(card[field])

    def test_identity_contains_expected_fields(self):
        identity = next(
            item["identity"]
            for item in self.fixture["items"]
            if item["type"] == 4
        )

        required_fields = {
            "firstName",
            "lastName",
            "address1",
            "city",
            "postalCode",
            "country",
            "email",
            "phone",
            "passportNumber",
            "licenseNumber",
        }

        self.assertTrue(
            required_fields.issubset(identity.keys())
        )

        for field in required_fields:
            self.assertIsInstance(identity[field], str)
            self.assertTrue(identity[field])

    def test_fixture_contains_custom_field_coverage(self):
        field_types = {
            field["type"]
            for item in self.fixture["items"]
            for field in item["fields"]
        }

        self.assertTrue({0, 1, 2}.issubset(field_types))


if __name__ == "__main__":
    unittest.main()
