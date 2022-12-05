"""Unit test for doxygen test extraction"""

import unittest
from pathlib import Path
from typing import List

import entries as en
from doxygen_util import extract_tests_from_functions


def get_by_text(all_tests: List[en.Test], name: str) -> en.Test:
    """Search function by name"""
    for test in all_tests:
        if test.text == name:
            return test
    raise Exception(f"No test found with name {name}")


class TestTestListFromDoxygen(unittest.TestCase):
    """Test for class"""

    def test_doxygen_test_matching(self):
        """Test"""

        all_tests = extract_tests_from_functions(Path("test/doxygen_tests"), "myid")

        # for t in all_functions:
        # print(t.name, t.file, t.line, t.statement)

        self.assertEqual(len(all_tests), 8)
        self.assertEqual(get_by_text(all_tests, "test1a").statement, "req-1a")
        self.assertEqual(get_by_text(all_tests, "test1b").statement, "req-1b")
        self.assertEqual(get_by_text(all_tests, "test2a").statement, "req-2a")
        self.assertEqual(get_by_text(all_tests, "test2b").statement, "req-2b")
        self.assertEqual(get_by_text(all_tests, "test3a").statement, "req-3a")
        self.assertEqual(get_by_text(all_tests, "test3b").statement, "req-3b")
        self.assertEqual(get_by_text(all_tests, "test4a").statement, "req-4a")
        self.assertEqual(get_by_text(all_tests, "test4b").statement, "req-4b")

        self.assertEqual(get_by_text(all_tests, "test1a").id, "myid-0")
        self.assertEqual(get_by_text(all_tests, "test1b").id, "myid-1")
        self.assertEqual(get_by_text(all_tests, "test2a").id, "myid-2")
        self.assertEqual(get_by_text(all_tests, "test2b").id, "myid-3")
        self.assertEqual(get_by_text(all_tests, "test3a").id, "myid-4")
        self.assertEqual(get_by_text(all_tests, "test3b").id, "myid-5")
        self.assertEqual(get_by_text(all_tests, "test4a").id, "myid-6")
        self.assertEqual(get_by_text(all_tests, "test4b").id, "myid-7")
