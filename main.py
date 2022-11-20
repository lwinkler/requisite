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
    exit(1)

# --------------------------------------------------------------------------------
def arguments_parser():
    """Define the parser and parse arguments"""

    # Main parser
    parser = argparse.ArgumentParser(
        description="Generate reports for a stock portfolio"
    )

    parser.add_argument(
        "input",
        type= Path,
        help="The input design in YAML format",
    )
    # arguments for QApplication
    parser.add_argument("--style", help="Passed to the constructor of QApplication")

    return parser.parse_args()

def print_design(design: du.Design) -> None:
    """Output the design"""
    print(f"{len(design.definitions)} definitions: ")
    print("\n".join([el.name for el in design.definitions]))
    print()
    print(f"{len(design.requirements)} requirements: ")
    print("\n".join([el.id for el in design.requirements]))
    print()
    print(f"{len(design.test_lists)} test lists: ")
    print("\n".join([el.name for el in design.test_lists]))
    print()
    all_tests = design.list_tests()
    print(f"{len(all_tests)} tests: ")
    print("\n".join([el.id for el in all_tests]))

if __name__ == "__main__":

    args = arguments_parser()

    design = yu.read_design(args.input)

    print_design(design)

    yu.write_design(Path("out.yaml"), design)
