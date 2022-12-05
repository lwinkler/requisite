#! env python3

""" Python main, instanciate all objects
@author: Laurent Winkler
@date: March 2019
@license: Boost
"""

import sys
import argparse
import unittest
from pathlib import Path

import yaml_util as yu
import entries  # pylint: disable=W0611
import expanders  # pylint: disable=W0611
import operations as op


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
    # arguments for QApplication
    parser.add_argument("--style", help="Passed to the constructor of QApplication")

    return parser.parse_args()


if __name__ == "__main__":

    args = arguments_parser()
    product_design = yu.read_design(args.input)
    product_design.expand(None)
    product_design.print()

    errors = op.check_all_rules(product_design)
    
    if errors:
        for message in messages:
            print("ERROR: ", message.related_id, message.text)
        exit(1)

    yu.write_design(Path("out.yaml"), product_design)

    test_loader = unittest.defaultTestLoader

    print(" ------------------------ ")

    for test_suite in test_loader.discover(".", pattern="test_*"):
        print("-", test_suite.countTestCases(), test_suite)
        # for test in test_loader.loadTestsFromTestSuite(test_suite):
        for test_case in test_suite._tests:  # pylint: disable=W0212
            print("  - ", test_case.countTestCases())
            print(890, test_loader.getTestCaseNames(test_case))
            print(890, test_loader.loadTestsFromModule(test_case))
            # for test_method in test_loader.loadTestsFromTestCase(test_case):
            for test_method in test_case._tests:  # pylint: disable=W0212
                print("    - ", "id", test_method.id(), test_method._testMethodDoc)
                # print(891, test_loader.getTestCaseNames(test_method))
                # print(890, test_loader.loadTestsFromModule(test_method))
                # pprint(vars(test_method))
