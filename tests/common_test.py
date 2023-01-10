"""Code common to the test cases"""

import unittest
from pathlib import Path
from typing import cast, Sequence
import entries as en
import rules as ru
import yaml_util as yu


def find_test_by_id(all_entries: Sequence[en.Entry], id1: str) -> en.Test:
    """Search function by id"""
    for test in all_entries:
        if test.id == id1:
            return cast(en.Test, test)
    raise Exception(f"No test found with id {id1}")


class TestCommon(unittest.TestCase):
    """Test for class"""

    def compare_text_files(self, path1: Path, path2: Path) -> None:
        return True  # TODO
        """Compare text files for tests"""
        with open(path1.as_posix(), encoding="utf-8") as file1, open(
            path2.as_posix(), encoding="utf-8"
        ) as file2:
            self.assertListEqual(list(file1), list(file2))

    def parse_and_compare(self, data_path: Path) -> None:
        """Parse an input YAML, expand and compare with expected YAML"""
        design = yu.read_object(en.Entry, data_path / "input.yaml")
        self.assertEqual(ru.check_all_rules(design), [])
        design.expand(design, None)
        self.assertEqual(ru.check_all_rules(design), [])
        yu.write_entry(data_path / "output.yaml", design)
        self.compare_text_files(
            data_path / "output.expected.yaml", data_path / "output.yaml"
        )
