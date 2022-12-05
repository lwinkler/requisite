"""Unit test for doxygen test extraction"""

import unittest
import yaml

import entries as en
import operations as op

DESIGN_STR1 = """
!Design
id: design-requisite
children:

# Requirements
- !Statement
  id: req-design-review
  text: A *design-document consists of one or several text files
  children:

  - !Statement
    id: spec-input-design
    text: A *design can be read from the *yaml-format

  - !Statement
    id: spec-design-split
    text: A *design can be split into several files

- !Statement
  id: req-design-output
  text: After processing the *expanded-design is written to output for future use
  children:

  - !Statement
    id: spec-design-output-yaml
    text: The *expanded-design can be written to *yaml-format

  - !Statement
    id: spec-design-output-markdown
    text: The *expanded-design can be written as a report to the *markdown-format

- !TestList
  id: tests-system
  children:

  - !Test
    id: test-design-review
    text: Verify that a design can be reviewed manually
    statement: req-design-review
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


class TestOperations(unittest.TestCase):
    """Test operations"""

    def test_extract_entries_of_type(self):
        """Test"""
        design1 = yaml.safe_load(DESIGN_STR1)

        designs = op.extract_entries_of_type(design1, en.Design)
        statements = op.extract_entries_of_type(design1, en.Statement)
        tests = op.extract_entries_of_type(design1, en.Test)

        self.assertEqual(len(designs), 1)
        self.assertEqual(
            ",".join([statement.id for statement in statements]),
            "req-design-review,spec-input-design,spec-design-split,"
            "req-design-output,spec-design-output-yaml,spec-design-output-markdown",
        )
        self.assertEqual(",".join([test.id for test in tests]), "test-design-review")

    def test_definition_id_mandatory(self) -> None:
        """Test verify spec-definition-id-mandatory"""
        design = yaml.safe_load(TEST_ID_MANDATORY)
        messages = op.check_definition_id_mandatory(design)
        self.assertEqual(messages, [
            op.ErrorMessage(related_id='', message='Definition id is missing'),
            op.ErrorMessage(related_id='', message='Definition id is missing')
            ])

    def test_statement_id_mandatory(self) -> None:
        """Test verify spec-statement-id-mandatory"""
        design = yaml.safe_load(TEST_ID_MANDATORY)
        messages = op.check_statement_id_mandatory(design)
        self.assertEqual(messages, [op.ErrorMessage(related_id='', message='Statement id is missing')])

    def test_id_unique(self) -> None:
        """Test verify spec-statement-id-mandatory"""
        design = yaml.safe_load(TEST_ID_UNIQUE)
        messages = op.check_id_unique(design)
        self.assertEqual(messages, [
            op.ErrorMessage(related_id='id-a', message='ID is duplicated'),
            op.ErrorMessage(related_id='id-b', message='ID is duplicated')
            ])

