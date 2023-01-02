"""Unit test for doxygen test extraction"""

import unittest
from typing import cast, Sequence

import entries as en
import operations as op
from verification import Verifier, VerificationType
import yaml_util as yu

TEST_VERIF = """
!Design
id: design-requisite1
children:

# Definitions
- !Definition
  id: def1
- !Definition
  id: def2

- !Statement
  id: stat-parent
  children:
  - !Requirement
    id: req-1
    children:
    - !Specification
        id: spec-2
        children:
        - !Specification
            id: spec-3
    - !Specification
        id: spec-4
  - !Specification
    id: spec-1
- !TestList
  children:
    - !Test
      verify_id: spec-1
    - !Test
      verify_id: spec-2
    - !Test
      verify_id: spec-3
"""


def get_by_id(all_statements: Sequence[en.Entry], id1: str) -> en.Statement:
    """Search function by id"""
    for test in all_statements:
        if test.id == id1:
            return cast(en.Statement, test)
    raise Exception(f"No test found with id {id1}")


class TestVerification(unittest.TestCase):
    """Test operations"""

    def test_verify(self) -> None:
        """Test"""

        design = yu.load_design(TEST_VERIF)
        verifier = Verifier(design)

        all_statements = op.extract_entries_of_type(design, en.Statement)
        self.assertEqual(
            verifier.verify(get_by_id(all_statements, "req-1")),
            [VerificationType.CHILDREN],
        )
        self.assertEqual(
            verifier.verify(get_by_id(all_statements, "spec-1")),
            [VerificationType.TEST],
        )
        self.assertEqual(
            verifier.verify(get_by_id(all_statements, "spec-2")),
            [VerificationType.TEST, VerificationType.CHILDREN],
        )
        self.assertEqual(
            verifier.verify(get_by_id(all_statements, "spec-3")),
            [VerificationType.TEST],
        )

    def test_spec_verify_statements(self) -> None:
        """Test list_verify and list_unverify as well as the matching specification"""

        design = yu.load_design(TEST_VERIF)
        verifier = Verifier(design)

        self.assertEqual(
            [entry.id for entry in verifier.list_verified(design)],
            ["stat-parent", "req-1", "spec-2", "spec-3", "spec-1"],
        )

        self.assertEqual(
            [entry.id for entry in verifier.list_unverified(design)], ["spec-4"]
        )
