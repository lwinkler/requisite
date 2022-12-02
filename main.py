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

    print_suite(test_loader.discover("."))

    print(" ------------------------ ")

    for t in test_loader.discover("."):
        print("-", t)
        for tt in t._tests:
            print("  - ", tt)
            for ttt in tt._tests:
                print("    - ", ttt._testMethodName, ttt)
                pprint(vars(ttt))
                print("...")
