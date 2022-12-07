"""Operations on design and entries"""

import re
from dataclasses import dataclass
from typing import List, Type

import entries as en


# def check_is_instance(entry: en.Entry, parent_class: Type) -> None:
# """Check if the object inherits from type (exception raised)"""
#
# if not isinstance(entry, parent_class):
# raise Exception(f"{entry.id} is not an instance of {parent_class.__name__}")
#
#
# def check_are_instances(entries: List[en.Entry], parent_class: Type) -> None:
# """Check if the objects inherit from type (exception raised)"""
# for entry in entries:
# check_is_instance(entry, parent_class)


@dataclass
class ErrorMessage:
    related_id: str
    text: str


def extract_entries_of_type(entry: en.Entry, parent_class: Type) -> List[en.Entry]:
    """Extract all instances that inherit from the type"""

    res: List[en.Entry] = []

    if isinstance(entry, parent_class):
        res.append(entry)

    if hasattr(entry, "children"):
        for child in entry.children:
            res += extract_entries_of_type(child, parent_class)

    return res


def check_all_rules(entry: en.Entry) -> List[ErrorMessage]:
    """Apply all existing rules to the entry and its children"""
    messages: List[ErrorMessage] = []
    messages += check_definition_id_mandatory(entry)
    messages += check_statement_id_mandatory(entry)
    messages += check_id_unique(entry)
    messages += check_id_valid(entry)
    messages += check_id_spec(entry)
    messages += check_id_req(entry)
    messages += check_links(entry)
    return messages


def check_definition_id_mandatory(entry: en.Entry) -> List[ErrorMessage]:
    """Check rule spec-definition-id-mandatory"""

    messages: List[ErrorMessage] = []
    for entry in extract_entries_of_type(entry, en.Definition):
        if not hasattr(entry, "id") or entry.id is None or not entry.id:
            messages.append(ErrorMessage("", "Definition id is missing"))
    return messages


def check_statement_id_mandatory(entry: en.Entry) -> List[ErrorMessage]:
    """Check rule spec-statement-id-mandatory"""

    messages: List[ErrorMessage] = []
    for entry in extract_entries_of_type(entry, en.Statement):
        if not hasattr(entry, "id") or entry.id is None or not entry.id:
            messages.append(ErrorMessage("", "Statement id is missing"))
    return messages


def check_id_unique(entry: en.Entry) -> List[ErrorMessage]:
    """Check rule spec-statement-id-unique"""

    known_ids: List[str] = []
    messages: List[ErrorMessage] = []

    for entry in extract_entries_of_type(entry, en.Entry):
        if hasattr(entry, "id") and entry.id is not None and entry.id:
            if entry.id in known_ids:
                messages.append(ErrorMessage(entry.id, "ID is duplicated"))
            else:
                known_ids.append(entry.id)
    return messages


def check_id_valid(entry: en.Entry) -> List[ErrorMessage]:
    """Check rule spec-statement-id-valid"""

    messages: List[ErrorMessage] = []

    for entry in extract_entries_of_type(entry, en.Entry):
        if hasattr(entry, "id") and entry.id is not None and entry.id:
            if not re.fullmatch("[a-zA-Z_][a-zA-Z0-9_-]*", entry.id):
                messages.append(
                    ErrorMessage(entry.id, "ID contains invalid characters")
                )
    return messages


def check_id_spec(entry: en.Entry) -> List[ErrorMessage]:
    """Check rule spec-statement-id-spec"""

    messages: List[ErrorMessage] = []

    for entry in extract_entries_of_type(entry, en.Specification):
        if hasattr(entry, "id") and entry.id is not None and entry.id:
            if not entry.id.startswith("spec-"):
                messages.append(
                    ErrorMessage(
                        entry.id, "ID of specification must start with 'spec-'"
                    )
                )
    return messages


def check_id_req(entry: en.Entry) -> List[ErrorMessage]:
    """Check rule spec-statement-id-req"""

    messages: List[ErrorMessage] = []
    for entry in extract_entries_of_type(entry, en.Requirement):
        if hasattr(entry, "id") and entry.id is not None and entry.id:
            if not entry.id.startswith("req-"):
                messages.append(
                    ErrorMessage(entry.id, "ID of requirement must start with 'req-'")
                )
    return messages


def check_links(entry: en.Entry) -> List[ErrorMessage]:
    """Check rule spec-statement-id-req"""

    all_ids = [entry.id for entry in extract_entries_of_type(entry, en.Entry)]
    messages: List[ErrorMessage] = []
    for entry in extract_entries_of_type(entry, en.Entry):
        links = entry.extract_links()
        for link in links:
            if link not in all_ids:
                messages.append(
                    ErrorMessage(entry.id, f"Linked id '{link}' does not exist.")
                )

    return messages


# - !Specification
# id: spec-valid-links
# text: The links in any text field of any *entry must be an existing entry id.
