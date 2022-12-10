"""Utilities for doxygen test parsing"""

import unittest

from typing import List, Union
from pathlib import Path
import entries as en
import expanders as ex


def extract_python_unittest_tests(path: Path, pattern: str) -> List[en.Entry]:
    """Extract the unit tests from python unittest module"""
    def extract_test_cases(
        test_suite_or_case: Union[unittest.TestSuite, unittest.TestCase],
    ) -> List[en.Entry]:
        if isinstance(test_suite_or_case, unittest.TestCase):
            print()
            return [
                en.Test(
                    test_suite_or_case.id(),
                    "TODO " + test_suite_or_case._testMethodDoc,  # pylint: disable=W0212
                    en.TestType.AUTOMATIC,
                    "TODO",
                )
            ]
        assert isinstance(test_suite_or_case, unittest.TestSuite)
        results = []
        for child in test_suite_or_case._tests:  # pylint: disable=W0212
            results += extract_test_cases(child)

        return results

    test_loader = unittest.defaultTestLoader
    return extract_test_cases(test_loader.discover(path.as_posix(), pattern=pattern))


class ExtractTestsFromPythonUnitTest(ex.Expander):
    """Extract tests written using the python unittest module"""

    yaml_tag = "!ExtractTestsFromPythonUnitTest"

    def __init__(  # pylint: disable=R0913
        self, id1: str, text: str, children: List[en.Entry], path: Path, pattern: str
    ):
        super().__init__(id1, text, children)
        self.path = path
        self.pattern = pattern

    def create_entries(self, parent: en.Entry) -> List[en.Entry]:
        return extract_python_unittest_tests(self.get_path(), self.pattern)

    def get_path(self) -> Path:
        """Return a Path object"""
        return Path(self.path)
