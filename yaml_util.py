"""Utilities for YAML file format"""

from pathlib import Path
from typing import List

import yaml
import design_util as du


def read_design(path: Path) -> du.Design:
    """Read a full design document in YAML format"""
    with open(path, encoding="utf-8") as fin:
        return yaml.safe_load(fin.read())


def read_entries(path: Path) -> List[du.Entry]:
    """Read a list of entries in YAML format"""
    with open(path, encoding="utf-8") as fin:
        return yaml.safe_load(fin.read())


def write_design(path: Path, design: du.Design) -> None:
    """Write a full design document in YAML format"""

    with open(path, "w", encoding="utf-8") as fout:
        # so far we set a very high line width
        fout.write(yaml.dump(design, width=1000))
