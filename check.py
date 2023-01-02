#! env python3

""" Requisite: Tools for the parsing and analysis of software specifications
@author: Laurent Winkler
@date: November 2022
@license: MIT
"""

import sys
import argparse
from pathlib import Path

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
        "-e",
        "--expand",
        action="store_true",
        help="Expand the design: will process all expander nodes, also file inclusion.",
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

    with open("specs/setup.py", encoding="utf-8") as file:
        exec(file.read())  # TODO

    args = arguments_parser()
    design = yu.read_design(args.input)
    print_errors(ru.check_all_rules(design))
    if args.expand:
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
