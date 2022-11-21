import unittest
from pathlib import Path
from design_util import DoxygenTestList


class TestDoxygenTestList(unittest.TestCase):
    """Test for class"""
    def test_doxygen_test_matching(self):

        tl = DoxygenTestList("my_test_list", Path("test/doxy_tests"))
        all_tests = tl.list_tests()
        print(1111, all_tests)
        # self.assertContain(all_tests,1)

