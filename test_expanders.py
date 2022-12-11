"""Unit test for expander classes"""

import unittest
from pathlib import Path
from typing import Any

import expanders
import yaml_util as yu
import common_test as ct

_ = expanders.Expander
del _



class TestExpanders(ct.TestCommon):
    """Test"""

    def test_spec_design_split(self) -> None:
        """Test"""
        self.parse_and_compare(Path("test/include"))

    def test_multiply_by_definition(self) -> None:
        """Test"""
        self.parse_and_compare(Path("test/multiply_by_definition"))
