"""Operations on design and entries"""

from typing import cast, TypeVar
import entries as en

T = TypeVar("T")


def extract_entries_of_type(entry: en.Entry, parent_class: type[T]) -> list[T]:
    """Extract all instances that inherit from the type"""

    res: list[T] = []

    if isinstance(entry, parent_class):
        res.append(entry)

    for child in entry.get_children():
        res += extract_entries_of_type(child, parent_class)

    return res


def find_entry_by_type_and_id(
    main_entry: en.Entry, parent_class: type[T], id1: str
) -> T:
    """Find an entry by type and id"""

    for entry in extract_entries_of_type(main_entry, parent_class):
        if cast(en.Entry, entry).get_id() == id1:
            return entry
    raise Exception(f"Cannot find entry of type {parent_class.__name__} and id {id1}")


def gather_all_ids(entry_to_check: en.Entry, parent_class: type[en.Entry]) -> list[str]:
    """Return all ids from the own and children entries"""
    all_ids: list[str] = []
    for entry in extract_entries_of_type(entry_to_check, parent_class):
        if entry.get_id():
            all_ids.append(entry.id)
    return all_ids
