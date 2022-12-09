"""Unit test for python unittest test extraction"""

import unittest
from pathlib import Path
from typing import List

import entries as en
import yaml_util as yu
from parsers.python_unittest import extract_python_unittest_tests


def get_by_id(all_tests: List[en.Test], id1: str) -> en.Test:
    """Search function by id"""
    for test in all_tests:
        if test.id == id1:
            return test
    raise Exception(f"No test found with id {id1}")


class TestTestListFromPythonUnitTest(unittest.TestCase):
    """Test for class"""

    def compare_text_files(self, path1: Path, path2: Path) -> None:
        """Compare text files for tests"""
        with open(path1.as_posix(), encoding="utf-8") as file1, open(
            path2.as_posix(), encoding="utf-8"
        ) as file2:
            self.assertListEqual(list(file1), list(file2))

    def test_python_unittest_test_matching(self):
        """Test"""

        all_tests = extract_python_unittest_tests(
            Path("parsers"), "test_python_unittest*"
        )

        # for test in all_tests:
            # print(111, test.id, test.verify_id)

        self.assertTrue(len(all_tests) > 0)
        self.assertEqual(
            get_by_id(
                all_tests,
                "parsers.test_python_unittest.TestTestListFromPythonUnitTest"
                ".test_extract_tests_from_python_unittest",
            ).verify_id,
            "req-1a",
        )
        self.assertEqual(
            get_by_id(
                all_tests,
                "parsers.test_python_unittest.TestTestListFromPythonUnitTest"
                ".test_python_unittest_test_matching",
            ).verify_id,
            "req-1a",
        )

    def test_extract_tests_from_python_unittest(self) -> None:
        """Test"""

        data_path = Path("test/python_unittest_tests")
        entries = yu.read_entries(data_path / "input1.yaml")
        for entry in entries:
            entry.expand(None)
        yu.write_entries(data_path / "output1.yaml", entries)
        self.compare_text_files(
            data_path / "expected1.yaml", data_path / "output1.yaml"
        )
