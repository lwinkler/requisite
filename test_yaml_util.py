"""Unit test for YAML serialization"""

import unittest
import yaml

import design_util as du

DESIGN_STR1 = """!Design
children:
- !Definition
  id: id3
  name: name3
  text: Some text
- !Statement
  id: id2
  name: name2
  text: Some text
id: design-id
"""


class TestYamlUtil(unittest.TestCase):
    """Test"""

    def test_serialize(self):
        """Test"""

        statement = du.Statement("id2", "name2", "Some text", None)
        definition = du.Definition("id3", "name3", "Some text", None)

        self.assertEqual(
            yaml.dump(statement, width=1000),
            "!Statement\nid: id2\nname: name2\ntext: Some text\n",
        )
        self.assertEqual(
            yaml.dump(definition, width=1000),
            "!Definition\nid: id3\nname: name3\ntext: Some text\n",
        )

    def test_unserialize(self):
        """Test"""

        statement = yaml.safe_load(
            "!Statement\nid: id2\nname: name2\ntext: Some text\n"
        )
        definition = yaml.safe_load(
            "!Definition\nid: id3\nname: name3\ntext: Some text\n"
        )

        self.assertEqual(statement.id, "id2")
        self.assertEqual(statement.name, "name2")

        self.assertEqual(definition.id, "id3")
        self.assertEqual(definition.name, "name3")

        self.assertEqual(
            yaml.dump(statement, width=1000),
            "!Statement\nid: id2\nname: name2\ntext: Some text\n",
        )
        self.assertEqual(
            yaml.dump(definition, width=1000),
            "!Definition\nid: id3\nname: name3\ntext: Some text\n",
        )

    def test_serialize_design(self):
        """Test"""

        statement = du.Statement("id2", "name2", "Some text", None)
        definition = du.Definition("id3", "name3", "Some text", None)
        design = du.Design("design-id", None, None, [definition] + [statement])

        self.assertEqual(yaml.dump(design, width=1000), DESIGN_STR1)

    def test_unserialize_design(self):
        """Test"""

        design = yaml.safe_load(DESIGN_STR1)

        self.assertTrue(isinstance(design.children[1], du.Statement))
        self.assertEqual(design.children[1].id, "id2")
        self.assertEqual(design.children[1].name, "name2")

        self.assertTrue(isinstance(design.children[0], du.Definition))
        self.assertEqual(design.children[0].id, "id3")
        self.assertEqual(design.children[0].name, "name3")

        self.assertEqual(yaml.dump(design, width=1000), DESIGN_STR1)
