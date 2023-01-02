"""Code related to test execution"""

from datetime import datetime
from enum import Enum
from typing import Sequence

import entries as en
import misc_util as mu
import operations as op


class TestResult(Enum):
    """The result of a test execution"""

    PASSED = "passed"
    SKIPPED = "skipped"
    FAILED = "failed"


class TestExecution(en.Entry):
    """The execution of a test"""

    short_type = "ex"
    yaml_tag = "!TestExecution"

    def __init__(self, test_id: str, date: str, result: TestResult):
        super().__init__("", "", [])  # TODO: is there a better way ?
        self.test_id = test_id
        self.date = date
        self.result = result


class TestListExecution(en.Entry):
    """The execution of a test list"""

    short_type = "lex"
    yaml_tag = "!TestListExecution"

    def __init__(
        self, test_list_id: str, date: str, children: Sequence[en.Entry], result: TestResult
    ):
        super().__init__("", "", children)  # TODO: is there a better way ?
        self.test_list_id = test_list_id
        self.date = date
        self.result = result


class TestEngine(en.Entry):
    """The test engine parent: subclass it to define how to run a test list"""
    short_type = "ten"
    yaml_tag = "!TestEngine"

    def __init__(self):
        super().__init__("", "", [])  # TODO: is there a better way ?

    def run_test_list(self, test_list: en.TestList) -> list[TestExecution]:
        """Run the tests of a test list"""
        results: list[TestExecution] = []
        for test in op.extract_entries_of_type(test_list, en.Test):
            result = self.run_test(test)
            results.append(
                TestExecution(
                    test.get_id(), mu.datetime_to_string(datetime.now()), result
                )
            )
        return results

    def run_test(self, test: en.Test) -> TestResult:
        """Run one test"""
        raise NotImplementedError()
