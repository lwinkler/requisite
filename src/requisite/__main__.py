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
    parser = argparse.ArgumentParser(description="Create a release folder")

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
        "-r",
        "--release-path",
        type=Path,
        help="The release directory. If empty it will be generated.",
    )

    parser.add_argument(
        "-R",
        "--releases-path",
        type=Path,
        help="The directory containing the releases. "
        "A subdirectory is automatically created with the current date.",
    )

    parser.add_argument(
        "--output-yaml",
        type=Path,
        help="Output the expanded design in YAML format and exit.",
    )

    parser.add_argument(
        "--report",
        type=Path,
        help="Write the design as a report and exit.",
    )
    return parser.parse_args()


def exit_if_errors(errors: Sequence[ru.EntryErrorMessage]) -> None:
    """Check for all syntax errors in design and abort on error"""

    for error in errors:
        print("ERROR: ", error.related_id, error.text, sys.stderr)
    if errors:
        sys.exit(1)


def generate_release_dir_path(path: Path) -> Path:
    """Generate the release dir path with current time stamp"""
    return path / mu.datetime_to_string(datetime.now())


def create_release(
    release_directory: Path, design: en.Design, verifier: ve.Verifier
) -> None:
    """Create a release in a directory"""

    print(f"Create a release in {release_directory.as_posix()}")

    if not release_directory.is_dir():
        print(f"Create release directory {release_directory.as_posix()}")
        os.makedirs(release_directory.as_posix())
        assert release_directory.is_dir()
        yu.write_entry(release_directory / "expanded_design.yaml", design)

    # TODO else warn if not identical
    # TODO: Add generation/expansion date to design
    # TODO: Add host information to test list
    # TODO: Write executions as separate files with timestamp, ... and keep an executions registry + date/author/host info
    # TODO: Allow to edit registry entry for manual testing

    executions = te.run_all_test_lists(design)
    for execution in executions:
        yu.write_entry(
            release_directory / (execution.test_list_id + ".yaml"), execution
        )

    print("Write report")
    rp.write_html_report(release_directory / "report.html", design, verifier)


def main() -> None:
    """Main routine of requisite"""
    args = arguments_parser()
    mu.import_source(args.setup)
    design = yu.read_object(en.Design, args.input)
    exit_if_errors(ru.check_all_rules(design))
    design.expand(design, None)
    exit_if_errors(ru.check_all_rules(design))

    verifier = ve.Verifier(design)
    unverified = verifier.list_unverified(design)

    if unverified:
        print(
            f"WARNING: The following {len(unverified)} statement(s) are not verified:",
            file=sys.stderr,
        )
        for statement in unverified:
            statement.print(sys.stderr)

    if args.output_yaml:
        print(f"Write {args.output_yaml.as_posix()}")
        yu.write_entry(args.output_yaml, design)
        sys.exit(0)

    if args.report:
        print(f"Write {args.report.as_posix()}")
        rp.write_html_report(args.report, design, verifier)
        sys.exit(0)

    if args.release_path:
        create_release(args.release_path, design, verifier)
        sys.exit(0)

    if args.releases_path:
        create_release(generate_release_dir_path(args.releases_path), design, verifier)
        sys.exit(0)

    print("No action was selected. Exiting.")


if __name__ == "__main__":
    main()
