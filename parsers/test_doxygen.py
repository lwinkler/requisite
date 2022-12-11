"""Unit test for doxygen test extraction"""

from pathlib import Path

import common_test as ct
from parsers.doxygen import extract_tests_from_functions


class TestTestListFromDoxygen(ct.TestCommon):
    """Test for class"""

    def test_doxygen_test_matching(self) -> None:
        """Test"""

        all_tests = extract_tests_from_functions(Path("test/doxygen_tests"))

        # for t in all_tests:
        # print(111, t.id, t.verify_id)

        self.assertEqual(len(all_tests), 8)
        self.assertEqual(
            ct.get_by_id(all_tests, "test1-simplest-cpp-test1a").verify_id, "req-1a"
        )
        self.assertEqual(
            ct.get_by_id(all_tests, "test1-simplest-cpp-test1b").verify_id, "req-1b"
        )
        self.assertEqual(
            ct.get_by_id(all_tests, "test1-simplest-cpp-test2a").verify_id, "req-2a"
        )
        self.assertEqual(
            ct.get_by_id(all_tests, "test1-simplest-cpp-test2b").verify_id, "req-2b"
        )
        self.assertEqual(
            ct.get_by_id(all_tests, "subdir-test2-simplest-cpp-test3a").verify_id,
            "req-3a",
        )
        self.assertEqual(
            ct.get_by_id(all_tests, "subdir-test2-simplest-cpp-test3b").verify_id,
            "req-3b",
        )
        self.assertEqual(
            ct.get_by_id(all_tests, "subdir-test2-simplest-cpp-test4a").verify_id,
            "req-4a",
        )
        self.assertEqual(
            ct.get_by_id(all_tests, "subdir-test2-simplest-cpp-test4b").verify_id,
            "req-4b",
        )

    def test_spec_extract_tests_doxygen_doc_format(self) -> None:
        """Test"""

        self.parse_and_compare(Path("test/doxygen_tests"))
