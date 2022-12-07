#! env python3

""" Requisite: Tools for the parsing and analysis of software specifications
@author: Laurent Winkler
@date: November 2022
@license: MIT
"""

import sys
import argparse
import unittest
from pathlib import Path

import yaml_util as yu
import entries
import expanders
import operations as op
import report as rp

# use modules to avoid warning
_ = (entries.Entry, expanders.Expander)
del _

if sys.version_info[0] < 3:
    print("Error: This script requires Python 3")
    sys.exit(1)


def arguments_parser():
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
        "-o",
        "--output",
        type=Path,
        help="Output the expanded design in YAML format.",
    )
    parser.add_argument(
        "-O",
        "--report",
        type=Path,
        help="Output the expanded design in a markdown format.",
    )

    return parser.parse_args()


def check_for_errors(product_design):
    """Check for all syntax errors in design and abort on error"""

    errors = op.check_all_rules(product_design)
    for error in errors:
        print("ERROR: ", error.related_id, error.text)
    if errors:
        sys.exit(1)

if __name__ == "__main__":

    args = arguments_parser()
    product_design = yu.read_design(args.input)
    check_for_errors(product_design)
    product_design.expand(None)
    check_for_errors(product_design)
    product_design.print()

    if args.output:
        print(f"Create {args.output.as_posix()}")
        yu.write_design(args.output, product_design)

    test_loader = unittest.defaultTestLoader

    if args.report:
        print(f"Create {args.report.as_posix()}")
        rp.write_html_report(args.report, product_design)


    print(" ------------------------ ")

    for test_suite in test_loader.discover(".", pattern="test_*"):
        print("-", test_suite.countTestCases(), test_suite)
        # for test in test_loader.loadTestsFromTestSuite(test_suite):
        if isinstance(test_suite, unittest.TestCase):
            print(111)
            continue
        for test_case in test_suite._tests:  # pylint: disable=W0212
            print("  - ", test_case.countTestCases())
            # for test_method in test_loader.loadTestsFromTestCase(test_case):
            if isinstance(test_case, unittest.TestCase):
                print(222)
                continue
            for test_method in test_case._tests:  # pylint: disable=W0212
                assert isinstance(test_method, unittest.TestCase)
                print("    - ", "id", test_method.id(), test_method._testMethodDoc)
                # print(891, test_loader.getTestCaseNames(test_method))
                # print(890, test_loader.loadTestsFromModule(test_method))
                # pprint(vars(test_method))
