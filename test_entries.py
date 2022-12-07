"""Unit test for doxygen test extraction"""

import unittest

import entries as en


class TestDesignUtil(unittest.TestCase):
    """Test"""

    def test_creation(self) -> None:
        """Test"""

        # entry = en.Entry("id1", "Some text", [])
        statement = en.Statement("id2", "Some text", [])
        definition = en.Definition("id3", "Some text", [])

        self.assertEqual(statement.id, "id2")

        self.assertEqual(definition.id, "id3")

    def test_extract_links(self):
        self.assertEqual(en.Entry("id", "My text without link", []).extract_links(), [])
        self.assertEqual(
            en.Entry("id", "My text <without link", []).extract_links(), []
        )
        self.assertEqual(
            en.Entry("id", "My text <without link<", []).extract_links(), []
        )
        self.assertEqual(
            en.Entry("id", "My text with one <simple> link", []).extract_links(),
            ["simple"],
        )
        self.assertEqual(
            en.Entry("id", "My text with one <simple> link>", []).extract_links(),
            ["simple"],
        )
        self.assertEqual(
            en.Entry("id", "My text with one <rather-tricky> link", []).extract_links(),
            ["rather-tricky"],
        )
        self.assertEqual(
            en.Entry("id", "My text with one <fake fake> link", []).extract_links(), []
        )
        self.assertEqual(
            en.Entry(
                "id", "My text with one <totally-Correct> link", []
            ).extract_links(),
            ["totally-Correct"],
        )
        self.assertEqual(
            en.Entry(
                "id", "My text with <many><links> that are <totally-correct>", []
            ).extract_links(),
            ["many", "links", "totally-correct"],
        )
        self.assertEqual(
            en.Entry(
                "id", "<many><links> that are <totally-correct>", []
            ).extract_links(),
            ["many", "links", "totally-correct"],
        )
