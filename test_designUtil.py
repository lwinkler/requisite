"""Unit test for doxygen test extraction"""

import unittest
from pathlib import Path
from typing import List

from design_util import *



class TestDesignUtil(unittest.TestCase):
    """Test"""

    def test_creation(self):
        """Test"""

        statement = Statement("id1", "name1", "Some text", None)
        requirement = Requirement("id2", "name2", "Some text", None)
        definition = Definition("id3", "name3", "Some text", None)


        self.assertEqual(requirement.id, "id2")
        self.assertEqual(requirement.name, "name2")

        self.assertEqual(definition.id, "id3")
        self.assertEqual(definition.name, "name3")
