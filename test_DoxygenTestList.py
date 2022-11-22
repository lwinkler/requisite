import unittest
from pathlib import Path
from design_util import DoxygenTestList, Function

def get_by_name(all_functions: Function, name: str) -> Function:
    for f in all_functions:
        if f.name == name:
            return f
    raise Exception(f"No function found with name {name}")

class TestDoxygenTestList(unittest.TestCase):
    """Test for class"""
    def test_doxygen_test_matching(self):

        tl = DoxygenTestList("my_test_list", Path("test/doxy_tests"))
        all_tests = tl.list_tests()

        # for t in all_tests:
            # print(t.name, t.file, t.line, t.requirement)

        self.assertEqual(len(all_tests), 8)
        self.assertEqual(get_by_name(all_tests, "test1a").requirement, "req-1a")
        self.assertEqual(get_by_name(all_tests, "test1b").requirement, "req-1b")
        self.assertEqual(get_by_name(all_tests, "test2a").requirement, "req-2a")
        self.assertEqual(get_by_name(all_tests, "test2b").requirement, "req-2b")
        self.assertEqual(get_by_name(all_tests, "test3a").requirement, "req-3a")
        self.assertEqual(get_by_name(all_tests, "test3b").requirement, "req-3b")
        self.assertEqual(get_by_name(all_tests, "test4a").requirement, "req-4a")
        self.assertEqual(get_by_name(all_tests, "test4b").requirement, "req-4b")

