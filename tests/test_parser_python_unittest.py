"""Unit test for python unittest test extraction"""

from pathlib import Path

import common_test as ct
from parser_python_unittest import extract_python_unittest_tests


class TestTestListFromPythonUnitTest(ct.TestCommon):
    """Test for class"""

    def test_parser_python_unittest_test_matching(self) -> None:
        """Test"""

        all_ids = ["req-asdf", "req-ffff", "spec-extract-tests-python-unittest-format"]
        all_tests = extract_python_unittest_tests(
            Path("tests"), "test_parser_python_unittest*", all_ids
        )

        # for test in all_tests:
        # print(111, test.id, test.verify_id)

        self.assertTrue(len(all_tests) > 0)
        self.assertEqual(
            ct.find_test_by_id(
                all_tests,
                "tests.test_parser_python_unittest.TestTestListFromPythonUnitTest"
                ".test_spec_extract_tests_python_unittest_format",
            ).verify_id,
            "spec-extract-tests-python-unittest-format",
        )

    def test_spec_extract_tests_python_unittest_format(self) -> None:
        """Test"""
        self.parse_and_compare(Path("tests/data/python_unittest_tests"))
