"""Operations on design and entries"""

from typing import List, Type

import design_util as du


# def check_is_instance(entry: du.Entry, parent_class: Type) -> None:
# """Check if the object inherits from type (exception raised)"""
#
# if not isinstance(entry, parent_class):
# raise Exception(f"{entry.id} is not an instance of {parent_class.__name__}")
#
#
# def check_are_instances(entries: List[du.Entry], parent_class: Type) -> None:
# """Check if the objects inherit from type (exception raised)"""
# for entry in entries:
# check_is_instance(entry, parent_class)


def extract_entries_of_type(entry: du.Entry, parent_class: Type) -> List[du.Entry]:
    """Extract all instances that inherit from the type"""

    res: List[du.Entry] = []

    if isinstance(entry, parent_class):
        res.append(entry)

    if hasattr(entry, "children"):
        for child in entry.children:
            res += extract_entries_of_type(child, parent_class)

    return res
