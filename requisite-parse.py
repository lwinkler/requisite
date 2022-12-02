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

from pprint import pprint

import yaml_util as yu


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


def print_suite(suite):
    """TODO"""
    if hasattr(suite, "__iter__"):
        for x in suite:
            print_suite(x)
        else:
            print(suite)


if __name__ == "__main__":

    args = arguments_parser()
    product_design = yu.read_design(args.input)
    product_design.expand()
    product_design.print()
    yu.write_design(Path("out.yaml"), product_design)

    test_loader = unittest.defaultTestLoader

    # print_suite(test_loader.discover(".", pattern="extra*"))
    #modules = test_loader.loadTestsFromModule()
    #print(modules)

    print(" ------------------------ ")

    for test_suite in test_loader.discover(".", pattern="test_*"):
        print("-", test_suite.countTestCases(), test_suite)
        #for test in test_loader.loadTestsFromTestSuite(test_suite):
        for test_case in test_suite._tests:
            print("  - ", test_case.countTestCases())
            print(890, test_loader.getTestCaseNames(test_case))
            print(890, test_loader.loadTestsFromModule(test_case))
            # for test_method in test_loader.loadTestsFromTestCase(test_case):
            for test_method in test_case._tests:
                print("    - ", "id", test_method.id(), test_method._testMethodDoc)
                # print(891, test_loader.getTestCaseNames(test_method))
                # print(890, test_loader.loadTestsFromModule(test_method))
                # pprint(vars(test_method))
