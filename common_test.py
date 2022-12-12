"""Code common to the test cases"""

import unittest
from pathlib import Path
from typing import List, cast
import entries as en
import operations as op
import yaml_util as yu


def get_by_id(all_tests: List[en.Entry], id1: str) -> en.Test:
    """Search function by id"""
    for test in all_tests:
        if test.id == id1:
            return cast(en.Test, test)
    raise Exception(f"No test found with id {id1}")


class TestCommon(unittest.TestCase):
    """Test for class"""

    def compare_text_files(self, path1: Path, path2: Path) -> None:
        """Compare text files for tests"""
        with open(path1.as_posix(), encoding="utf-8") as file1, open(
            path2.as_posix(), encoding="utf-8"
        ) as file2:
            self.assertListEqual(list(file1), list(file2))

    def parse_and_compare(self, data_path: Path) -> None:
        design = yu.read_design(data_path / "input.yaml")
        self.assertEqual(op.check_all_rules(design), [])
        design.expand(design, None)
        self.assertEqual(op.check_all_rules(design), [])
        yu.write_design(data_path / "output.yaml", design)
        self.compare_text_files(
            data_path / "output.expected.yaml", data_path / "output.yaml"
        )
