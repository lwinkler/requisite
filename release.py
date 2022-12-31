#! env python3

""" Run a test suite """

import os
import sys
import argparse
import yaml
from datetime import datetime
from pathlib import Path
from typing import List

import yaml_util as yu
import entries as en
import operations as op
import expanders
import rules as ru
import report as rp
import verification as ve
import parsers.doxygen
import parsers.python_unittest

# use modules to avoid warning
_ = (
    expanders.Expander,
    parsers.doxygen.ExtractTestsFromDoxygen,
    parsers.python_unittest.ExtractTestsFromPythonUnitTest,
)
del _

if sys.version_info[0] < 3:
    print("Error: This script requires Python 3")
    sys.exit(1)


def arguments_parser() -> argparse.Namespace:
    """Define the parser and parse arguments"""

    # Main parser
    parser = argparse.ArgumentParser(
        description="Generate reports for a stock portfolio"
    )

    parser.add_argument(
        "input",
        type=Path,
        help="The input design in YAML format",
    )

    parser.add_argument(
        "-d", "--test_dir",
        type=Path,
        help="The test directory. If empty it will be generated.",
    )
    return parser.parse_args()


def check_for_errors(design1: en.Design) -> None:
    """Check for all syntax errors in design and abort on error"""

    errors = ru.check_all_rules(design1)
    for error in errors:
        print("ERROR: ", error.related_id, error.text)
    if errors:
        sys.exit(1)

def datetime_to_string(dt: datetime) -> str:
    """Convert datetime into a string"""
    return dt.strftime('%Y-%m-%d.%H%M%S')

def generate_test_dir_path(releases_path: Path) -> Path:
    """Generate the test dir path with current time stamp"""
    return releases_path / datetime_to_string(datetime.now())


# -----

class TestExecution(en.Entry):
    """The execution of a test"""

    short_type = "ex"
    yaml_tag = "!TestExecution"

    def __init__(self, test_id: str, date: str, result: str):
        super().__init__("", "", []) # TODO: is there a better way ?
        self.test_id = test_id
        self.date = date
        self.result = result

class TestListExecution(en.Entry):
    """The execution of a test list"""

    short_type = "lex"
    yaml_tag = "!TestListExecution"

    def __init__(self, test_list_id: str, date: str, children: List[TestExecution], result: str):
        super().__init__("", "", children) # TODO: is there a better way ?
        self.test_list_id = test_list_id
        self.date = date
        self.result = result

class TestEngine: # (en.Entry):

    # short_type = "ten"
    # yaml_tag = "!TestEngine"

    def run_test_list(self, test_list: en.TestList) -> List[TestExecution]:
        """Run the tests of a test list"""
        results : List[TestExecution] = []
        for test in op.extract_entries_of_type(test_list, en.Test):
            result = self.run_test(test)
            results.append(TestExecution(test.get_id(), datetime_to_string(datetime.now()), result))
        return results

    def run_test(self, test: en.Test) -> str:
        """Run one test"""
        return "TODO"


if __name__ == "__main__":

    args = arguments_parser()
    design = yu.read_design(args.input)
    check_for_errors(design)
    design.expand(design, None)
    check_for_errors(design)


    releases_path = Path(".") / "releases"
    test_directory = args.test_dir if args.test_dir else generate_test_dir_path(releases_path)
    if not test_directory.is_dir():
        print(f"Create output directory {test_directory.as_posix()}")
        if not releases_path.is_dir():
            os.mkdir(releases_path)

        os.mkdir(test_directory.as_posix())
        yu.write_entry(test_directory / "expanded_design.yml", design)
    # TODO else warn if not identical
    # TODO: Add generation/expansion date to design
    assert releases_path in test_directory.parents



    verifier = ve.Verifier(design)
    # unverified = verifier.list_unverified(design)

    engine = TestEngine()
    for entry in op.extract_entries_of_type(design, en.TestList):
        test_executions = engine.execute_test_list(entry)
        test_list_execution = TestListExecution(entry.get_id(), datetime_to_string(datetime.now()), test_executions, "TODO")
        yu.write_entry(test_directory / (entry.get_id() + ".yaml"), test_list_execution)


    
    print(f"Create report")
    rp.write_html_report(test_directory / "report.html", design, verifier)
