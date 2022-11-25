#! env python3

""" Python main, instanciate all objects
@author: Laurent Winkler
@date: March 2019
@license: Boost
"""

import sys
import argparse
from pathlib import Path

import yaml_util as yu
import design_util as du


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


def print_design(design: du.Design) -> None:
    """Output the design"""
    print("design:")
    print("  statements:")
    for element in design.statements:
        print("    " + str(element))
    all_tests = design.list_tests()
    # print(f"{len(all_tests)} tests: ")
    # print("\n".join([element.id for element in all_tests]))


if __name__ == "__main__":

    args = arguments_parser()
    product_design = yu.read_design(args.input)
    print_design(product_design)
    yu.write_design(Path("out.yaml"), product_design)
