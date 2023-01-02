"""Utilities for YAML file format"""

from pathlib import Path
from typing import cast

import yaml
import entries as en


def read_entry(path: Path) -> en.Entry:
    """Read a full design document in YAML format"""
    with open(path, encoding="utf-8") as fin:
        return cast(en.Entry, yaml.safe_load(fin.read()))


def read_design(path: Path) -> en.Design:
    """Read a full design document in YAML format"""
    return cast(en.Design, read_entry(path))


def load_design(str_value: str) -> en.Design:
    """Read a full design document in YAML format"""
    return cast(en.Design, load_entry(str_value))


def load_entry(str_value: str) -> en.Entry:
    """Read a full design document in YAML format"""
    return cast(en.Entry, yaml.safe_load(str_value))


def read_entries(path: Path) -> list[en.Entry]:
    """Read a list of entries in YAML format"""
    with open(path, encoding="utf-8") as fin:
        return cast(list[en.Entry], yaml.safe_load(fin.read()))


def dump_entry(entry: en.Entry) -> str:
    """Dump and entry to a string"""
    return cast(str, yaml.dump(entry, width=1000, sort_keys=False))


def write_entry(path: Path, design: en.Entry) -> None:
    """Write a full design document in YAML format"""

    design.simplify()

    with open(path, "w", encoding="utf-8") as fout:
        # so far we set a very high line width
        fout.write(dump_entry(design))


# def write_entries(path: Path, entries: list[en.Entry]) -> None:
# """Write a full design document in YAML format"""
#
# for entry in entries:
# entry.simplify()
#
# with open(path, "w", encoding="utf-8") as fout:
# # so far we set a very high line width
# fout.write(yaml.dump(entries, width=1000, sort_keys=False)))
