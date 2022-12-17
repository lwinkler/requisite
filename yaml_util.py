"""Utilities for YAML file format"""

from pathlib import Path
from typing import List, cast

import yaml
import entries as en


def read_design(path: Path) -> en.Design:
    """Read a full design document in YAML format"""
    with open(path, encoding="utf-8") as fin:
        return cast(en.Design, yaml.safe_load(fin.read()))

def load_entry(str_value: str) -> en.Entry:
    """Read a full design document in YAML format"""
    return yaml.safe_load(str_value)

def read_entries(path: Path) -> List[en.Entry]:
    """Read a list of entries in YAML format"""
    with open(path, encoding="utf-8") as fin:
        return cast(List[en.Entry], yaml.safe_load(fin.read()))

def dump_entry(entry: en.Entry) -> str:

    return yaml.dump(entry, width=1000, sort_keys=False)

def write_design(path: Path, design: en.Design) -> None:
    """Write a full design document in YAML format"""

    design.simplify()

    with open(path, "w", encoding="utf-8") as fout:
        # so far we set a very high line width
        fout.write(dump_entry(design))


# def write_entries(path: Path, entries: List[en.Entry]) -> None:
# """Write a full design document in YAML format"""
#
# for entry in entries:
# entry.simplify()
#
# with open(path, "w", encoding="utf-8") as fout:
# # so far we set a very high line width
# fout.write(yaml.dump(entries, width=1000, sort_keys=False)))
