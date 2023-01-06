"""Utilities for YAML file format"""

from pathlib import Path
from typing import cast, TypeVar

import yaml
import entries as en

T = TypeVar("T")


def read_object(_: type[T], path: Path) -> T:
    """Read a full design document in YAML format"""
    with open(path, encoding="utf-8") as fin:
        return cast(T, yaml.safe_load(fin.read()))

def read_object_from_string(_: type[T], str1: str) -> T:
    """Read a full design document in YAML format"""
    return cast(T, yaml.safe_load(str1))


def load_object(_: type[T], str_value: str) -> T:
    """Read a full design document in YAML format"""
    return cast(T, yaml.safe_load(str_value))


def read_objects(_: type[T], path: Path) -> list[T]:
    """Read a list of entries in YAML format"""
    with open(path, encoding="utf-8") as fin:
        return cast(list[T], yaml.safe_load(fin.read()))


def dump_entry(entry: en.Entry) -> str:
    """Dump and entry to a string"""
    # so far we set a very high line width
    return cast(str, yaml.dump(entry, width=1000, sort_keys=False))


def write_entry(path: Path, design: en.Entry) -> None:
    """Write a full full design or entry in YAML format"""

    design.simplify()

    with open(path, "w", encoding="utf-8") as fout:
        fout.write(dump_entry(design))
