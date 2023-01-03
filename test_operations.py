"""Unit test for operations.py"""

import unittest
from typing import cast

import entries as en
import operations as op
import yaml_util as yu

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

- !Section
  children:
  - !TestList
    id: tests-system
    children:
    - !Test
      id: test-design-review
      text: Verify that a design can be reviewed manually
      verify_id: req-design-review
"""


class TestOperations(unittest.TestCase):
    """Test operations"""

    def test_extract_entries_of_type(self) -> None:
        """Test function"""
        design1 = yu.load_entry(DESIGN_STR1)

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

    def test_find_entry_by_type_and_id(self) -> None:
        """Test function"""
        design = yu.load_entry(DESIGN_STR1)

        entry = op.find_entry_by_type_and_id(design, en.Entry, "test-design-review")
        self.assertEqual(cast(en.Test, entry).verify_id, "req-design-review")

        entry = op.find_entry_by_type_and_id(design, en.Test, "test-design-review")
        self.assertEqual(entry.verify_id, "req-design-review")

        def failing() -> None:
            op.find_entry_by_type_and_id(design, en.Statement, "test-design-review")

        self.assertRaises(Exception, failing)
