"""Operations on design and entries"""

import re
from dataclasses import dataclass
from typing import List

import entries as en
import expanders as ex


def extract_entries_of_type(
    entry: en.Entry, parent_class: type[en.Entry]
) -> List[en.Entry]:
    """Extract all instances that inherit from the type"""

    res: List[en.Entry] = []

    if isinstance(entry, parent_class):
        res.append(entry)

    for child in entry.get_children():
        res += extract_entries_of_type(child, parent_class)

    return res


def find_entry_by_type_and_id(
    main_entry: en.Entry, parent_class: type[en.Entry], id1: str
) -> en.Entry:
    """Find an entry by type and id"""

    # TODO Test
    for entry in extract_entries_of_type(main_entry, parent_class):
        if entry.id == id1:
            return entry
    raise Exception(f"Cannot find entry of type {parent_class.__name__} and id {id1}")


def gather_all_ids(entry_to_check: en.Entry, parent_class: type[en.Entry]) -> List[str]:
    """Return all ids from the own and children entries"""
    all_ids: List[str] = []
    for entry in extract_entries_of_type(entry_to_check, parent_class):
        if entry.get_id():
            all_ids.append(entry.id)
    return all_ids


