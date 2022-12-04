"""Unit test for doxygen test extraction"""

import io
import unittest
from pathlib import Path

import design_util as du
import yaml_util as yu


class TestDesignUtil(unittest.TestCase):
    """Test"""

    def test_creation(self) -> None:
        """Test"""

        # entry = du.Entry("id1", "Some text", [])
        statement = du.Statement("id2", "Some text", [])
        definition = du.Definition("id3", "Some text", [])

        self.assertEqual(statement.id, "id2")

        self.assertEqual(definition.id, "id3")
