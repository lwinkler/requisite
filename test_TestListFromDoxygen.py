"""Unit test for doxygen test extraction"""

import unittest
from pathlib import Path
from typing import List

from doxygen_util import extract_tests_from_functions, Function


def get_by_name(all_functions: List[Function], name: str) -> Function:
    """Search function by name"""
    for func in all_functions:
        if func.name == name:
            return func
    raise Exception(f"No function found with name {name}")


class TestTestListFromDoxygen(unittest.TestCase):
    """Test for class"""

    def test_doxygen_test_matching(self):
        """Test"""

        all_functions = extract_tests_from_functions(Path("test/doxygen_tests"))

        # for t in all_functions:
        # print(t.name, t.file, t.line, t.statement)

        self.assertEqual(len(all_functions), 8)
        self.assertEqual(get_by_name(all_functions, "test1a").statement, "req-1a")
        self.assertEqual(get_by_name(all_functions, "test1b").statement, "req-1b")
        self.assertEqual(get_by_name(all_functions, "test2a").statement, "req-2a")
        self.assertEqual(get_by_name(all_functions, "test2b").statement, "req-2b")
        self.assertEqual(get_by_name(all_functions, "test3a").statement, "req-3a")
        self.assertEqual(get_by_name(all_functions, "test3b").statement, "req-3b")
        self.assertEqual(get_by_name(all_functions, "test4a").statement, "req-4a")
        self.assertEqual(get_by_name(all_functions, "test4b").statement, "req-4b")
