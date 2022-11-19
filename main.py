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
        "--debug",
        action="store_true",
        dest="debug",
        default=False,
        help="Run the application with faulthandler to debug crashes and segmentation faults. Installed with 'pip3 install faulthandler' ",
    )
    # arguments for QApplication
    parser.add_argument("--style", help="Passed to the constructor of QApplication")

    return parser.parse_args()


if __name__ == "__main__":

    options = arguments_parser()

    design = yu.read_design(Path("test/data/design_confstruct.yaml"))

    print(design.requirements)
    print(design.definitions)

    print(
        f"Read {len(design.requirements)} requirements and {len(design.definitions)} definitions"
    )

    el = design.requirements[0]

    print(el)

    yu.write_design(Path("out.yaml"), design)
