"""Unit test for doxygen test extraction"""

import unittest
import yaml

import operations as op
import design_util as du

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
  name: System tests
  children:

  - !Test
    id: test-design-review
    text: Verify that a design can be reviewed manually
    statement: req-design-review
"""


class TestOperations(unittest.TestCase):
    """Test operations"""

    def test_check_are_instances(self):
        """Test"""
        # TODO: Remove ??

    def test_extract_entries_of_type(self):
        design1 = yaml.safe_load(DESIGN_STR1)

        designs = op.extract_entries_of_type(design1, du.Design)
        statements = op.extract_entries_of_type(design1, du.Statement)
        tests = op.extract_entries_of_type(design1, du.Test)

        self.assertEqual(len(designs), 1)
        self.assertEqual(
            ",".join([statement.id for statement in statements]),
            "req-design-review,spec-input-design,spec-design-split,"
            "req-design-output,spec-design-output-yaml,spec-design-output-markdown",
        )
        self.assertEqual(",".join([test.id for test in tests]), "test-design-review")
