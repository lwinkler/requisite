"""Code related to test execution"""

from datetime import datetime
from enum import Enum

import entries as en
import misc_util as mu
import operations as op
from typing import Tuple


class TestResult(Enum):
    """The result of a test execution"""

    SUCCESS = "success"
    SKIPPED = "skipped"
    FAILED = "failed"


class TestExecution(en.Entry):
    """The execution of a test"""

    short_type = "ex"
    yaml_tag = "!TestExecution"

    def __init__(
        self, test_id: str, date: str, result: TestResult, stdout: str, stderr: str
    ):
        super().__init__("", "", [])
        self.test_id = test_id
        self.date = date
        self.result = result.value
        self.stdout = stdout
        self.stderr = stderr


class TestListExecution(en.Entry):
    """The execution of a test list"""

    short_type = "lex"
    yaml_tag = "!TestListExecution"

    def __init__(
        self,
        test_list_id: str,
        date: str,
        children: list[en.Entry],
        result: TestResult,
    ):
        super().__init__("", "", children)
        self.test_list_id = test_list_id
        self.date = date
        self.result = result.value


class TestEngine(en.Entry):
    """The test engine parent: subclass it to define how to run a test list"""

    short_type = "ten"
    yaml_tag = "!TestEngine"

    def __init__(self, id1: str, text: str) -> None:
        super().__init__(id1, text, [])

    def run_test_list(self, test_list: en.TestList) -> list[TestExecution]:
        """Run the tests of a test list"""
        results: list[TestExecution] = []
        for test in op.extract_entries_of_type(test_list, en.Test):
            timestamp = mu.datetime_to_string(datetime.now())
            result, stdout, stderr = self.run_test(test)
            results.append(
                TestExecution(test.get_id(), timestamp, result, stdout, stderr)
            )
        return results

    def run_test(self, test: en.Test) -> Tuple[TestResult, str, str]:
        """Run one test"""
        raise NotImplementedError()


def run_all_test_lists(design: en.Design) -> list[TestListExecution]:
    """Run all the test lists"""
    test_list_executions = []
    for entry in op.extract_entries_of_type(design, en.TestList):
        test_executions = entry.engine.run_test_list(entry)
        test_list_executions.append(
            TestListExecution(
                entry.get_id(),
                mu.datetime_to_string(datetime.now()),
                test_executions,
                TestResult.SKIPPED,  # TODO
            )
        )
    return test_list_executions
