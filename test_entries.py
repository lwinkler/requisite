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
