"""Unit test for doxygen test extraction"""

import unittest
from pathlib import Path
from typing import List

import entries as en
import yaml_util as yu
from parsers.doxygen import extract_tests_from_functions


def get_by_id(all_tests: List[en.Test], id1: str) -> en.Test:
    """Search function by id"""
    for test in all_tests:
        if test.get_id() == id1:
            return test
    raise Exception(f"No test found with id {id1}")


class TestTestListFromDoxygen(unittest.TestCase):
    """Test for class"""

    def compare_text_files(self, path1: Path, path2: Path) -> None:
        """Compare text files for tests"""
        with open(path1.as_posix(), encoding="utf-8") as file1, open(
            path2.as_posix(), encoding="utf-8"
        ) as file2:
            self.assertListEqual(list(file1), list(file2))

    def test_doxygen_test_matching(self):
        """Test"""

        all_tests = extract_tests_from_functions(Path("test/doxygen_tests"), "myid")

        # for t in all_tests:
            # print(111, t.id, t.verify_id)

        self.assertEqual(len(all_tests), 8)
        self.assertEqual(get_by_id(all_tests, "test1-simplest-cpp-test1a").verify_id, "req-1a")
        self.assertEqual(get_by_id(all_tests, "test1-simplest-cpp-test1b").verify_id, "req-1b")
        self.assertEqual(get_by_id(all_tests, "test1-simplest-cpp-test2a").verify_id, "req-2a")
        self.assertEqual(get_by_id(all_tests, "test1-simplest-cpp-test2b").verify_id, "req-2b")
        self.assertEqual(get_by_id(all_tests, "subdir-test2-simplest-cpp-test3a").verify_id, "req-3a")
        self.assertEqual(get_by_id(all_tests, "subdir-test2-simplest-cpp-test3b").verify_id, "req-3b")
        self.assertEqual(get_by_id(all_tests, "subdir-test2-simplest-cpp-test4a").verify_id, "req-4a")
        self.assertEqual(get_by_id(all_tests, "subdir-test2-simplest-cpp-test4b").verify_id, "req-4b")

    def test_extract_tests_from_doxygen(self) -> None:
        """Test"""

        data_path = Path("test/doxygen_tests")
        entries = yu.read_entries(data_path / "input1.yaml")
        for entry in entries:
            entry.expand(None)
        yu.write_entries(data_path / "output1.yaml", entries)
        self.compare_text_files(
            data_path / "expected1.yaml", data_path / "output1.yaml"
        )
