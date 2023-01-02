#! env python3

""" Run a test suite """

import os
import sys
import argparse
from datetime import datetime
from pathlib import Path
from typing import Sequence

import yaml_util as yu
import entries as en
import operations as op
import misc_util as mu
import testing as te
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
        "-d",
        "--test_dir",
        type=Path,
        help="The test directory. If empty it will be generated.",
    )
    return parser.parse_args()


def print_errors(errors: Sequence[ru.EntryErrorMessage]) -> None:
    """Check for all syntax errors in design and abort on error"""

    for error in errors:
        print("ERROR: ", error.related_id, error.text)
    if errors:
        sys.exit(1)


def generate_test_dir_path(path: Path) -> Path:
    """Generate the test dir path with current time stamp"""
    return path / mu.datetime_to_string(datetime.now())


# -----


if __name__ == "__main__":


    args = arguments_parser()
    mu.import_source(args.setup)
    design = yu.read_design(args.input)
    print_errors(ru.check_all_rules(design))
    design.expand(design, None)
    print_errors(ru.check_all_rules(design))

    releases_path = Path(".") / "releases"
    test_directory = (
        args.test_dir if args.test_dir else generate_test_dir_path(releases_path)
    )
    if not test_directory.is_dir():
        print(f"Create output directory {test_directory.as_posix()}")
        if not releases_path.is_dir():
            os.mkdir(releases_path)

        os.mkdir(test_directory.as_posix())
        yu.write_entry(test_directory / "expanded_design.yml", design)
    # TODO else warn if not identical
    # TODO: Add generation/expansion date to design
    assert releases_path in test_directory.parents

    verifier = ve.Verifier(design)
    # unverified = verifier.list_unverified(design)

    # TODO: Move this code ?
    for entry in op.extract_entries_of_type(design, en.TestList):
        test_executions = entry.engine.run_test_list(entry)
        test_list_execution = te.TestListExecution(
            entry.get_id(),
            mu.datetime_to_string(datetime.now()),
            test_executions,
            te.TestResult.SKIPPED,  # TODO
        )
        yu.write_entry(test_directory / (entry.get_id() + ".yaml"), test_list_execution)

    print("Create report")
    rp.write_html_report(test_directory / "report.html", design, verifier)
