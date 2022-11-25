"""Unit test for YAML serialization"""

import unittest
from pathlib import Path
from typing import List

from yaml_util import *
from design_util import *

design_str1 = """!Design
definitions:
- !Definition
  id: id3
  name: name3
  text: Some text
requirements:
- !Requirement
  id: id2
  name: name2
  text: Some text
test_lists: []
"""


class TestDesignUtil(unittest.TestCase):
    """Test"""

    def test_serialize(self):
        """Test"""

        # statement = Statement("id1", "name1", "Some text")
        requirement = Requirement("id2", "name2", "Some text")
        definition = Definition("id3", "name3", "Some text")

        # self.assertEqual(yaml.dump(statement, width=1000), '!Statement\nid: id1\nname: name1\ntext: Some text\n')
        self.assertEqual(yaml.dump(requirement, width=1000), '!Requirement\nid: id2\nname: name2\ntext: Some text\n')
        self.assertEqual(yaml.dump(definition, width=1000), '!Definition\nid: id3\nname: name3\ntext: Some text\n')

    def test_unserialize(self):
        """Test"""

        requirement = yaml.safe_load('!Requirement\nid: id2\nname: name2\ntext: Some text\n')
        definition = yaml.safe_load('!Definition\nid: id3\nname: name3\ntext: Some text\n')

        self.assertEqual(requirement.id, "id2")
        self.assertEqual(requirement.name, "name2")

        self.assertEqual(definition.id, "id3")
        self.assertEqual(definition.name, "name3")


        self.assertEqual(yaml.dump(requirement, width=1000), '!Requirement\nid: id2\nname: name2\ntext: Some text\n')
        self.assertEqual(yaml.dump(definition, width=1000), '!Definition\nid: id3\nname: name3\ntext: Some text\n')

    def test_serialize_design(self):
        """Test"""

        requirement = Requirement("id2", "name2", "Some text")
        definition = Definition("id3", "name3", "Some text")
        design = Design([definition], [requirement], [])

        self.assertEqual(yaml.dump(design, width=1000), design_str1)

    def test_unserialize_design(self):
        """Test"""

        design = yaml.safe_load(design_str1)

        self.assertTrue(isinstance(design.requirements[0], Requirement))
        self.assertEqual(design.requirements[0].id, "id2")
        self.assertEqual(design.requirements[0].name, "name2")

        self.assertTrue(isinstance(design.definitions[0], Definition))
        self.assertEqual(design.definitions[0].id, "id3")
        self.assertEqual(design.definitions[0].name, "name3")

        self.assertEqual(yaml.dump(design, width=1000), design_str1)
