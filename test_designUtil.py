"""Unit test for doxygen test extraction"""

import unittest

import design_util as du


class TestDesignUtil(unittest.TestCase):
    """Test"""

    def test_creation(self):
        """Test"""

        # statement = du.Statement("id1", "name1", "Some text", None)
        requirement = du.Requirement("id2", "name2", "Some text", None)
        definition = du.Definition("id3", "name3", "Some text", None)

        self.assertEqual(requirement.id, "id2")
        self.assertEqual(requirement.name, "name2")

        self.assertEqual(definition.id, "id3")
        self.assertEqual(definition.name, "name3")
