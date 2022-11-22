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

        all_functions = extract_tests_from_functions(Path("test/doxy_tests"))

        # for t in all_functions:
        # print(t.name, t.file, t.line, t.requirement)

        self.assertEqual(len(all_functions), 8)
        self.assertEqual(get_by_name(all_functions, "test1a").requirement, "req-1a")
        self.assertEqual(get_by_name(all_functions, "test1b").requirement, "req-1b")
        self.assertEqual(get_by_name(all_functions, "test2a").requirement, "req-2a")
        self.assertEqual(get_by_name(all_functions, "test2b").requirement, "req-2b")
        self.assertEqual(get_by_name(all_functions, "test3a").requirement, "req-3a")
        self.assertEqual(get_by_name(all_functions, "test3b").requirement, "req-3b")
        self.assertEqual(get_by_name(all_functions, "test4a").requirement, "req-4a")
        self.assertEqual(get_by_name(all_functions, "test4b").requirement, "req-4b")
