"""Unit test for YAML serialization"""

import unittest
from pathlib import Path

import entries as en
import expanders as ex
import yaml_util as yu

import parsers.python_unittest

DESIGN_STR1 = """!Design
id: design-id
children:
- !Definition
  id: id3
  text: Some text
- !Statement
  id: id2
  text: Some text
"""


class TestYamlUtil(unittest.TestCase):
    """Test"""

    def entry_read_write(self, str_value: str, object_type: type[en.Entry]) -> None:
        """Test the serialization of an entry"""
        entry = yu.load_entry(str_value)
        self.assertEqual(type(entry), object_type)
        self.assertEqual(str_value, yu.dump_entry(entry))

    def test_serialize(self) -> None:
        """Test"""

        statement = en.Statement("id2", "Some text", [])
        definition = en.Definition("id3", "Some text", [])

        statement.simplify()
        self.assertEqual(
            yu.dump_entry(statement),
            "!Statement\nid: id2\ntext: Some text\n",
        )
        definition.simplify()
        self.assertEqual(
            yu.dump_entry(definition),
            "!Definition\nid: id3\ntext: Some text\n",
        )

    def test_unserialize(self) -> None:
        """Test"""

        statement = yu.load_entry("!Statement\nid: id2\ntext: Some text\n")
        definition = yu.load_entry("!Definition\nid: id3\ntext: Some text\n")

        self.assertEqual(statement.id, "id2")
        self.assertEqual(definition.id, "id3")

        statement.simplify()
        self.assertEqual(
            yu.dump_entry(statement),
            "!Statement\nid: id2\ntext: Some text\n",
        )
        definition.simplify()
        self.assertEqual(
            yu.dump_entry(definition),
            "!Definition\nid: id3\ntext: Some text\n",
        )

    def test_serialize_design(self) -> None:
        """Test"""

        statement = en.Statement("id2", "Some text", [])
        definition = en.Definition("id3", "Some text", [])
        design = en.Design("design-id", "", [definition] + [statement])

        design.simplify()
        self.assertEqual(yu.dump_entry(design), DESIGN_STR1)

    def test_unserialize_design(self) -> None:
        """Test"""

        design = yu.load_entry(DESIGN_STR1)

        self.assertTrue(isinstance(design.children[1], en.Statement))
        self.assertEqual(design.children[1].id, "id2")

        self.assertTrue(isinstance(design.children[0], en.Definition))
        self.assertEqual(design.children[0].id, "id3")

        design.simplify()
        self.assertEqual(yu.dump_entry(design), DESIGN_STR1)

    def test_spec_design_output_yaml(self) -> None:
        """Test"""
        design = yu.read_design(Path("specs/requisite.yaml"))
        design.expand(design, None)
        self.assertTrue(yu.dump_entry(design) != "")

    def test_spec_input_entries_entry(self) -> None:
        """Test"""
        self.entry_read_write(
            """!Entry
id: myid
text: My text
children:
- !Entry
  id: child-id
""",
            en.Entry,
        )

    def test_spec_input_entries_design(self) -> None:
        """Test"""
        self.entry_read_write(
            """!Design
id: myid
text: My text
children:
- !Entry
  id: child-id
""",
            en.Design,
        )

    def test_spec_input_entries_section(self) -> None:
        """Test"""
        self.entry_read_write(
            """!Section
id: myid
text: My text
children:
- !Entry
  id: child-id
""",
            en.Section,
        )

    def test_spec_input_entries_expander(self) -> None:
        """Test"""
        self.entry_read_write(
            """!Expander
id: myid
text: My text
children:
- !Entry
  id: child-id
""",
            ex.Expander,
        )

    def test_spec_input_entries_definition(self) -> None:
        """Test"""
        self.entry_read_write(
            """!Definition
id: myid
text: My text
children:
- !Entry
  id: child-id
""",
            en.Definition,
        )

    def test_spec_input_entries_statement(self) -> None:
        """Test"""
        self.entry_read_write(
            """!Statement
id: myid
text: My text
children:
- !Entry
  id: child-id
""",
            en.Statement,
        )

    def test_spec_input_entries_requirement(self) -> None:
        """Test"""
        self.entry_read_write(
            """!Requirement
id: myid
text: My text
children:
- !Entry
  id: child-id
""",
            en.Requirement,
        )

    def test_spec_input_entries_specification(self) -> None:
        """Test"""
        self.entry_read_write(
            """!Specification
id: myid
text: My text
children:
- !Entry
  id: child-id
""",
            en.Specification,
        )

    def test_spec_input_entries_test(self) -> None:
        """Test"""
        self.entry_read_write(
            """!Test
id: myid
text: My text
type: manual
verify_id: spec-some-spec
children:
- !Entry
  id: child-id
""",
            en.Test,
        )

    def test_spec_input_entries_test_list(self) -> None:
        """Test"""
        self.entry_read_write(
            """!TestList
id: myid
engine: my_engine
text: My text
children:
- !Entry
  id: child-id
""",
            en.TestList,
        )
