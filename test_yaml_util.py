"""Unit test for YAML serialization"""

import unittest
import yaml

import entries as en

DESIGN_STR1 = """!Design
children:
- !Definition
  id: id3
  text: Some text
- !Statement
  id: id2
  text: Some text
id: design-id
"""


class TestYamlUtil(unittest.TestCase):
    """Test"""

    def test_serialize(self):
        """Test"""

        statement = en.Statement("id2", "Some text", None)
        definition = en.Definition("id3", "Some text", None)

        statement.simplify()
        self.assertEqual(
            yaml.dump(statement, width=1000),
            "!Statement\nid: id2\ntext: Some text\n",
        )
        definition.simplify()
        self.assertEqual(
            yaml.dump(definition, width=1000),
            "!Definition\nid: id3\ntext: Some text\n",
        )

    def test_unserialize(self):
        """Test"""

        statement = yaml.safe_load("!Statement\nid: id2\ntext: Some text\n")
        definition = yaml.safe_load("!Definition\nid: id3\ntext: Some text\n")

        self.assertEqual(statement.id, "id2")

        self.assertEqual(definition.id, "id3")

        statement.simplify()
        self.assertEqual(
            yaml.dump(statement, width=1000),
            "!Statement\nid: id2\ntext: Some text\n",
        )
        definition.simplify()
        self.assertEqual(
            yaml.dump(definition, width=1000),
            "!Definition\nid: id3\ntext: Some text\n",
        )

    def test_serialize_design(self):
        """Test"""

        statement = en.Statement("id2", "Some text", None)
        definition = en.Definition("id3", "Some text", None)
        design = en.Design("design-id", None, [definition] + [statement])

        design.simplify()
        self.assertEqual(yaml.dump(design, width=1000), DESIGN_STR1)

    def test_unserialize_design(self):
        """Test"""

        design = yaml.safe_load(DESIGN_STR1)

        self.assertTrue(isinstance(design.children[1], en.Statement))
        self.assertEqual(design.children[1].id, "id2")

        self.assertTrue(isinstance(design.children[0], en.Definition))
        self.assertEqual(design.children[0].id, "id3")

        design.simplify()
        self.assertEqual(yaml.dump(design, width=1000), DESIGN_STR1)
