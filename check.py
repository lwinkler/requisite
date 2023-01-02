#! env python3

""" Requisite: Tools for the parsing and analysis of software specifications
@author: Laurent Winkler
@date: November 2022
@license: MIT
"""

import sys
import argparse
from pathlib import Path

import misc_util as mu
import yaml_util as yu
import rules as ru
import report as rp
import verification as ve


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
        "setup",
        type=Path,
        help="The setup.py file that imports the python classes needed by the design",
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


def print_errors(errors: list[ru.EntryErrorMessage]) -> None:
    """Check for all syntax errors in design and abort on error"""

    for error in errors:
        print("ERROR: ", error.related_id, error.text)
    if errors:
        sys.exit(1)


if __name__ == "__main__":

    args = arguments_parser()
    mu.import_source(args.setup)
    design = yu.read_design(args.input)
    print_errors(ru.check_all_rules(design))
    design.expand(design, None)
    print_errors(ru.check_all_rules(design))
    # design.print()

    if args.output:
        print(f"Create {args.output.as_posix()}")
        yu.write_entry(args.output, design)

    verifier = ve.Verifier(design)
    unverified = verifier.list_unverified(design)

    if args.report:
        print(f"Create {args.report.as_posix()}")
        rp.write_html_report(args.report, design, verifier)

    print(
        f"WARNING: The following {len(unverified)} statement(s) are not verified:",
        file=sys.stderr,
    )
    for statement in unverified:
        statement.print(sys.stderr)
