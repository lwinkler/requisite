"""Unit test for expander classes"""

import unittest
from pathlib import Path

import expanders
import yaml_util as yu

_ = expanders.Expander
del _


class TestExpanders(unittest.TestCase):
    """Test"""

    def compare_text_files(self, path1: Path, path2: Path) -> None:
        """Compare text files for tests"""
        with open(path1.as_posix(), encoding="utf-8") as file1, open(
            path2.as_posix(), encoding="utf-8"
        ) as file2:
            self.assertListEqual(list(file1), list(file2))

    def test_include(self) -> None:
        """Test"""

        data_path = Path("test/include")
        entries = yu.read_entries(data_path / "input1.yaml")
        for entry in entries:
            entry.expand(None)
        yu.write_entries(data_path / "output1.yaml", entries)
        self.compare_text_files(
            data_path / "expected1.yaml", data_path / "output1.yaml"
        )
