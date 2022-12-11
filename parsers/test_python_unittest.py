"""Unit test for python unittest test extraction"""

import unittest
from pathlib import Path
from typing import List, Any, cast

import entries as en
import yaml_util as yu
from parsers.python_unittest import extract_python_unittest_tests


def parse_and_compare(test_object: Any, data_path: Path) -> None:
        design = yu.read_design(data_path / "input.yaml")
        design.expand(design, None)
        yu.write_design(data_path / "output.yaml", design)
        test_object.compare_text_files(
            data_path / "output.expected.yaml", data_path / "output.yaml"
        )

def get_by_id(all_tests: List[en.Entry], id1: str) -> en.Test:
    """Search function by id"""
    for test in all_tests:
        if test.id == id1:
            return cast(en.Test, test)
    raise Exception(f"No test found with id {id1}")


class TestTestListFromPythonUnitTest(unittest.TestCase):
    """Test for class"""

    def compare_text_files(self, path1: Path, path2: Path) -> None:
        """Compare text files for tests"""
        with open(path1.as_posix(), encoding="utf-8") as file1, open(
            path2.as_posix(), encoding="utf-8"
        ) as file2:
            self.assertListEqual(list(file1), list(file2))

    def test_python_unittest_test_matching(self) -> None:
        """Test"""
        
        all_ids = ["req-asdf", "req-ffff", "spec-extract-tests-python-unittest-format"]
        all_tests = extract_python_unittest_tests(
            Path("."), "test_python_unittest*", all_ids
        )

        # for test in all_tests:
            # print(111, test.id, test.verify_id)

        self.assertTrue(len(all_tests) > 0)
        self.assertEqual(
            get_by_id(
                all_tests,
                "parsers.test_python_unittest.TestTestListFromPythonUnitTest"
                ".test_spec_extract_tests_python_unittest_format",
            ).verify_id,
            "spec-extract-tests-python-unittest-format",
        )

    def test_spec_extract_tests_python_unittest_format(self) -> None:
        """Test"""
        parse_and_compare(self, Path("test/python_unittest_tests"))

