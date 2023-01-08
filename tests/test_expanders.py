"""Unit test for expander classes"""

from pathlib import Path
import common_test as ct

import expanders

_ = expanders.Expander
del _


class TestExpanders(ct.TestCommon):
    """Test"""

    def test_spec_design_split(self) -> None:
        """Test"""
        self.parse_and_compare(Path("tests/data/include"))

    def test_multiply_by_definition(self) -> None:
        """Test"""
        self.parse_and_compare(Path("tests/data/multiply_by_definition"))
