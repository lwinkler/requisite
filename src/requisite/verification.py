"""Verification of design"""

from enum import Enum
from typing import Sequence
import entries as en
import operations as op


class VerificationType(Enum):
    """How a statement can be verified"""

    TEST = "test"
    CHILDREN = "children"


class Verifier:
    """Object that contains the verification information of the design"""

    def __init__(self, design: en.Design):
        self.verified_ids = [
            test.verify_id for test in op.extract_entries_of_type(design, en.Test)
        ]

    def verify(self, statement: en.Statement) -> Sequence[VerificationType]:
        """Verify a statement"""
        results: list[VerificationType] = []
        if statement.id in self.verified_ids:
            results.append(VerificationType.TEST)
        if statement.get_children():
            results.append(VerificationType.CHILDREN)
        return results

    def list_verified(self, design: en.Entry) -> Sequence[en.Statement]:
        """List all verified statements"""
        all_statements = op.extract_entries_of_type(design, en.Statement)
        return [statement for statement in all_statements if self.verify(statement)]

    def list_unverified(self, design: en.Entry) -> Sequence[en.Statement]:
        """List all verified statements"""
        all_statements = op.extract_entries_of_type(design, en.Statement)
        return [statement for statement in all_statements if not self.verify(statement)]
