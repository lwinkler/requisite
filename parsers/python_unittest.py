"""Utilities for doxygen test parsing"""

import unittest

from typing import Union, Optional
from pathlib import Path
import entries as en
import expanders as ex
import operations as op

TEST_PREFIX = "test_"


def extract_verify_id_from_function_name(
    name: str, all_ids: list[str]
) -> Optional[str]:
    """Extract the statement id from the function name"""

    def simplify_id(id1: str) -> str:
        return id1.replace("-", "").replace("_", "").lower()

    assert name.startswith(TEST_PREFIX)
    simplified_id = simplify_id(name[len(TEST_PREFIX) :])
    possible_ids: list[str] = []
    for id1 in all_ids:
        if simplify_id(id1) == simplified_id:
            possible_ids.append(id1)

    if len(possible_ids) > 1:
        raise Exception(
            f"More than one statement match test method name '{name}: '",
            possible_ids,
            " Please change one of those ids.",
        )

    return possible_ids[0] if len(possible_ids) == 1 else None


def extract_python_unittest_tests(
    path: Path, pattern: str, all_ids: list[str]
) -> list[en.Entry]:
    """Extract the unit tests from python unittest module"""

    def extract_test_cases(
        test_suite_or_case: Union[unittest.TestSuite, unittest.TestCase],
    ) -> list[en.Entry]:
        if isinstance(test_suite_or_case, unittest.TestCase):
            verify_id = extract_verify_id_from_function_name(
                test_suite_or_case._testMethodName, all_ids  # pylint: disable=W0212
            )
            return (
                []
                if verify_id is None
                else [
                    en.Test(
                        test_suite_or_case.id(),
                        test_suite_or_case._testMethodDoc,  # pylint: disable=W0212
                        en.TestType.AUTOMATIC,
                        verify_id,
                    )
                ]
            )
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
        self, id1: str, text: str, children: list[en.Entry], path: Path, pattern: str
    ):
        super().__init__(id1, text, children)
        self.path = path
        self.pattern = pattern

    def create_entries(self, design: en.Entry, parent: en.Entry) -> list[en.Entry]:
        all_ids = op.gather_all_ids(design, en.Statement)
        return extract_python_unittest_tests(self.get_path(), self.pattern, all_ids)

    def get_path(self) -> Path:
        """Return a Path object"""
        return Path(self.path)
