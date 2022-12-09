#! env python3

""" Requisite: Tools for the parsing and analysis of software specifications
@author: Laurent Winkler
@date: November 2022
@license: MIT
"""

import sys
import argparse
from pathlib import Path
from typing import List

import yaml_util as yu
import entries as en
import expanders
import operations as op
import report as rp
import parsers.doxygen
import parsers.python_unittest as pu

# use modules to avoid warning
_ = (expanders.Expander, parsers.doxygen.ExtractTestsFromDoxygen)
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


def check_for_errors(design: en.Design):
    """Check for all syntax errors in design and abort on error"""

    errors = op.check_all_rules(design)
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


    if args.report:
        print(f"Create {args.report.as_posix()}")
        rp.write_html_report(args.report, product_design)

    print(" ------------------------ ")

    tests = pu.extract_python_unittest_tests(Path("."), "test_*")
    for test in tests:
        test.print()


