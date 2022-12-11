"""Unit test for expander classes"""

import unittest
from pathlib import Path
from typing import Any

import expanders
import yaml_util as yu

_ = expanders.Expander
del _

def parse_and_compare(test_object: Any, data_path: Path) -> None:
        design = yu.read_design(data_path / "input.yaml")
        design.expand(design, None)
        yu.write_design(data_path / "output.yaml", design)
        test_object.compare_text_files(
            data_path / "output.expected.yaml", data_path / "output.yaml"
        )

class TestExpanders(unittest.TestCase):
    """Test"""

    def compare_text_files(self, path1: Path, path2: Path) -> None:
        """Compare text files for tests"""
        with open(path1.as_posix(), encoding="utf-8") as file1, open(
            path2.as_posix(), encoding="utf-8"
        ) as file2:
            self.assertListEqual(list(file1), list(file2))

    def test_spec_design_split(self) -> None:
        """Test"""
        parse_and_compare(self, Path("test/include"))

    def test_multiply_by_definition(self) -> None:
        """Test"""
        parse_and_compare(self, Path("test/multiply_by_definition"))
