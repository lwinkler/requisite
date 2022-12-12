"""Unit test for rules.py"""

import unittest
import yaml
from typing import List, Any

import entries as en
import rules as ru


TEST_ID_NON_NULL = """
!Design
id: design-requisite
children:

# Definitions
- !Definition
  id:
  text: The document that specifies the design

- !Definition
  id: expanded-design
  text: The full design, after entries have been expanded

- !Definition
  id: formats
  text: All file formats for input and output
  children:

  - !Definition
    text: The YAML format, used for input and output.

  - !Definition
    id: markdown-format
    text: The Markdown format to generate documents, reports, ...

- !TestList
  text:   
  children:
  - !Test
    id: my-test
    verify_id:

"""

TEST_ID_MANDATORY = """
!Design
id: design-requisite
children:

# Definitions
- !Definition
  text: The document that specifies the design

- !Definition
  id: expanded-design
  text: The full design, after entries have been expanded

- !Definition
  id: formats
  text: All file formats for input and output
  children:

  - !Definition
    text: The YAML format, used for input and output.

  - !Definition
    id: markdown-format
    text: The Markdown format to generate documents, reports, ...

- !Statement
  text: Some statement

"""

TEST_ID_UNIQUE = """
!Design
id: design-requisite
children:

# Definitions
- !Definition
  id: id-a
  text: The document that specifies the design

- !Definition
  id: id-b
  text: The full design, after entries have been expanded

- !Definition
  id: id-a
  text: All file formats for input and output
  children:

  - !Definition
    id: id-B
    text: The YAML format, used for input and output.

  - !Definition
    id: id-b
    text: The Markdown format to generate documents, reports, ...

- !Statement
  id: id-c
  text: Some statement
"""

TEST_ID_VALID = """
!Design
id: design-requisite1
children:

# Definitions
- !Definition
  id: id%
- !Definition
  id: expanded$-design

- !Definition
  id: MYID
  children:
  - !Definition
    id: 44z
  - !Definition
    id: maRkdown-format
  - !Definition
    id: ma.kdown-format
- !Statement
  id: пр44
- !Statement
  id: a
"""

TEST_ID_PREF = """
!Design
id: design-requisite1
children:

- !Specification
  id: spec-12aaa
  children:
  - !Requirement
    id: 44z
  - !Specification
    id: req-format
- !Requirement
  id: req-abc-asdf
- !Requirement
  id: req_abc
"""

TEST_LINKS = """
!Design
id: design-requisite1
text: Link with <asdf>s
children:

- !Specification
  id: asdf
  children:
  - !Requirement
    id: 44z
  - !Specification
    id: req-format
    text: <Text> with a failing link and a successful <one>
- !Section
  children:
  - !Requirement
    id: req-abc-asdf
    text: <another> text with a failing link and a successful <one>
  - !Requirement
    id: one
"""


class TestRules(unittest.TestCase):

    def check_rule(self, func: Any, design_str: str, expected_messages: List[ru.ErrorMessage]):
        """Test any checking function"""
        design = yaml.safe_load(design_str)
        messages = func(design)
        self.assertListEqual(messages, expected_messages)
        # check that global check also finds our messages
        messages = ru.check_all_rules(design)
        for msg in expected_messages:
            self.assertIn(msg, messages)

    def test_spec_entry_attributes_non_null(self) -> None:
        """Test spec-entry-attributes-non-null"""
        self.check_rule(ru.check_entry_attributes_non_null, TEST_ID_NON_NULL, [
            ru.ErrorMessage(related_id="", text="Entry attribute id has a null value"),
            ru.ErrorMessage(
                related_id="", text="Entry attribute text has a null value"
            ),
            ru.ErrorMessage(
                related_id="my-test", text="Entry attribute verify_id has a null value"
            ),
        ])

    def test_spec_definition_id_mandatory(self) -> None:
        """Test verify spec-definition-id-mandatory"""
        self.check_rule(ru.check_definition_id_mandatory, TEST_ID_MANDATORY, [
            ru.ErrorMessage(related_id="", text="Definition id is missing"),
            ru.ErrorMessage(related_id="", text="Definition id is missing"),
        ])

    def test_spec_statement_id_mandatory(self) -> None:
        """Test verify spec-statement-id-mandatory"""
        self.check_rule(ru.check_statement_id_mandatory, TEST_ID_MANDATORY, [
            ru.ErrorMessage(related_id="", text="Statement id is missing")
        ])

    def test_spec_id_unique(self) -> None:
        """Test verify spec-id-unique"""
        self.check_rule(ru.check_id_unique, TEST_ID_UNIQUE, [
            ru.ErrorMessage(related_id="id-a", text="ID is duplicated"),
            ru.ErrorMessage(related_id="id-b", text="ID is duplicated"),
        ])

    def test_spec_id_valid_chars(self) -> None:
        """Test verify spec-id-valid-chars"""
        self.check_rule(ru.check_id_valid, TEST_ID_VALID, [
            ru.ErrorMessage(related_id="id%", text="ID contains invalid characters"),
            ru.ErrorMessage(
                related_id="expanded$-design", text="ID contains invalid characters"
            ),
            ru.ErrorMessage(related_id="44z", text="ID contains invalid characters"),
            ru.ErrorMessage(related_id="пр44", text="ID contains invalid characters"),
        ])

    def test_spec_id_spec(self) -> None:
        """Test verify spec-id-spec"""
        self.check_rule(ru.check_id_spec, TEST_ID_PREF, [
            ru.ErrorMessage(
                related_id="req-format",
                text="ID of specification must start with 'spec-'",
            )
        ])

    def test_spec_id_req(self) -> None:
        """Test verify spec-id-req"""
        self.check_rule(ru.check_id_req, TEST_ID_PREF, [
            ru.ErrorMessage(
                related_id="44z", text="ID of requirement must start with 'req-'"
            ),
            ru.ErrorMessage(
                related_id="req_abc", text="ID of requirement must start with 'req-'"
            ),
        ])

    def test_spec_valid_links(self) -> None:
        """Test verify spec-valid-links"""
        self.check_rule(ru.check_links, TEST_LINKS, [
            ru.ErrorMessage(
                related_id="req-format", text="Linked id 'Text' does not exist."
            ),
            ru.ErrorMessage(
                related_id="req-abc-asdf",
                text="Linked id 'another' does not exist.",
            ),
        ])
