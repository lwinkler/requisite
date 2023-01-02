"""Code related to test execution"""

from datetime import datetime

import entries as en
import operations as op


def datetime_to_string(dt: datetime) -> str:
    """Convert datetime into a string"""
    return dt.strftime("%Y-%m-%d.%H%M%S")


class TestExecution(en.Entry):
    """The execution of a test"""

    short_type = "ex"
    yaml_tag = "!TestExecution"

    def __init__(self, test_id: str, date: str, result: str):
        super().__init__("", "", [])  # TODO: is there a better way ?
        self.test_id = test_id
        self.date = date
        self.result = result


class TestListExecution(en.Entry):
    """The execution of a test list"""

    short_type = "lex"
    yaml_tag = "!TestListExecution"

    def __init__(
        self, test_list_id: str, date: str, children: list[en.Entry], result: str
    ):
        super().__init__("", "", children)  # TODO: is there a better way ?
        self.test_list_id = test_list_id
        self.date = date
        self.result = result


class TestEngine:  # (en.Entry):

    # short_type = "ten"
    # yaml_tag = "!TestEngine"

    def run_test_list(self, test_list: en.TestList) -> list[TestExecution]:
        """Run the tests of a test list"""
        results: list[TestExecution] = []
        for test in op.extract_entries_of_type(test_list, en.Test):
            result = self.run_test(test)
            results.append(
                TestExecution(test.get_id(), datetime_to_string(datetime.now()), result)
            )
        return results

    def run_test(self, test: en.Test) -> str:
        """Run one test"""
        raise NotImplementedError()
