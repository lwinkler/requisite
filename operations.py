"""Operations on design and entries"""

import re
from dataclasses import dataclass
from typing import List

import entries as en
import expanders as ex


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
    """Error messages returned by checks"""

    related_id: str
    text: str


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
        if hasattr(entry, "id") and entry.id:
            all_ids.append(entry.id)
    return all_ids


def check_all_rules(entry: en.Entry) -> List[ErrorMessage]:
    """Apply all existing rules to the entry and its children"""
    messages = check_entry_attributes_non_null(entry)
    messages += check_definition_id_mandatory(entry)
    messages += check_statement_id_mandatory(entry)
    messages += check_id_unique(entry)
    messages += check_id_valid(entry)
    messages += check_id_spec(entry)
    messages += check_id_req(entry)
    messages += check_links(entry)
    messages += check_child_statements(entry)
    messages += check_child_definition(entry)
    messages += check_child_test(entry)
    messages += check_test_statement_id(entry)
    return messages


def check_entry_attributes_non_null(entry_to_check: en.Entry) -> List[ErrorMessage]:
    """Check rule spec-entry-attributes-non-null"""

    messages: List[ErrorMessage] = []
    # TODO: Children
    for entry in extract_entries_of_type(entry_to_check, en.Entry):
        for attribute_name in entry.__dict__.keys():
            if (
                hasattr(entry, attribute_name)
                and getattr(entry, attribute_name) is None
            ):
                messages.append(
                    ErrorMessage(
                        entry.get_id(),
                        f"Entry attribute {attribute_name} has a null value",
                    )
                )
    return messages


def check_definition_id_mandatory(entry_to_check: en.Entry) -> List[ErrorMessage]:
    """Check rule spec-definition-id-mandatory"""

    messages: List[ErrorMessage] = []
    for entry in extract_entries_of_type(entry_to_check, en.Definition):
        if not hasattr(entry, "id") or entry.id is None or not entry.id:
            messages.append(ErrorMessage("", "Definition id is missing"))
    return messages


def check_statement_id_mandatory(entry_to_check: en.Entry) -> List[ErrorMessage]:
    """Check rule spec-statement-id-mandatory"""

    messages: List[ErrorMessage] = []
    for entry in extract_entries_of_type(entry_to_check, en.Statement):
        if not hasattr(entry, "id") or entry.id is None or not entry.id:
            messages.append(ErrorMessage("", "Statement id is missing"))
    return messages


def check_id_unique(entry_to_check: en.Entry) -> List[ErrorMessage]:
    """Check rule spec-statement-id-unique"""

    known_ids: List[str] = []
    messages: List[ErrorMessage] = []

    for entry in extract_entries_of_type(entry_to_check, en.Entry):
        if hasattr(entry, "id") and entry.id is not None and entry.id:
            if entry.id in known_ids:
                messages.append(ErrorMessage(entry.id, "ID is duplicated"))
            else:
                known_ids.append(entry.id)
    return messages


def check_id_valid(entry_to_check: en.Entry) -> List[ErrorMessage]:
    """Check rule spec-statement-id-valid"""

    messages: List[ErrorMessage] = []

    for entry in extract_entries_of_type(entry_to_check, en.Entry):
        if hasattr(entry, "id") and entry.id is not None and entry.id:
            if not re.fullmatch("[a-zA-Z_][a-zA-Z0-9_.-]*", entry.id):
                messages.append(
                    ErrorMessage(entry.id, "ID contains invalid characters")
                )
    return messages


def check_id_spec(entry_to_check: en.Entry) -> List[ErrorMessage]:
    """Check rule spec-statement-id-spec"""

    messages: List[ErrorMessage] = []

    for entry in extract_entries_of_type(entry_to_check, en.Specification):
        if hasattr(entry, "id") and entry.id is not None and entry.id:
            if not entry.id.startswith("spec-"):
                messages.append(
                    ErrorMessage(
                        entry.id, "ID of specification must start with 'spec-'"
                    )
                )
    return messages


def check_id_req(entry_to_check: en.Entry) -> List[ErrorMessage]:
    """Check rule spec-statement-id-req"""

    messages: List[ErrorMessage] = []
    for entry in extract_entries_of_type(entry_to_check, en.Requirement):
        if hasattr(entry, "id") and entry.id is not None and entry.id:
            if not entry.id.startswith("req-"):
                messages.append(
                    ErrorMessage(entry.id, "ID of requirement must start with 'req-'")
                )
    return messages


def check_links(entry_to_check: en.Entry) -> List[ErrorMessage]:
    """Check rule spec-statement-id-req"""

    all_ids = gather_all_ids(entry_to_check, en.Entry)

    messages: List[ErrorMessage] = []
    for entry in extract_entries_of_type(entry_to_check, en.Entry):
        links = entry.extract_links()
        for link in links:
            if link not in all_ids:
                messages.append(
                    ErrorMessage(entry.id, f"Linked id '{link}' does not exist.")
                )

    return messages


def check_child_statements(entry_to_check: en.Entry) -> List[ErrorMessage]:
    """Check rule spec-child-statement"""

    messages: List[ErrorMessage] = []
    for entry in extract_entries_of_type(entry_to_check, en.Statement):
        for child in entry.get_children():
            if not isinstance(child, en.Statement) and not isinstance(
                child, ex.Expander
            ):
                messages.append(
                    ErrorMessage(
                        entry.id, "Statement can only have statements as children"
                    )
                )

    return messages


def check_child_definition(entry_to_check: en.Entry) -> List[ErrorMessage]:
    """Check rule spec-child-definition"""

    messages: List[ErrorMessage] = []
    for entry in extract_entries_of_type(entry_to_check, en.Definition):
        for child in entry.get_children():
            if not isinstance(child, en.Definition) and not isinstance(
                child, ex.Expander
            ):
                messages.append(
                    ErrorMessage(
                        entry.id, "Definition can only have definitions as children"
                    )
                )

    return messages


def check_child_test(entry_to_check: en.Entry) -> List[ErrorMessage]:
    """Check rule spec-child-test-list"""

    messages: List[ErrorMessage] = []
    for entry in extract_entries_of_type(entry_to_check, en.TestList):
        for child in entry.get_children():
            if not isinstance(child, en.Test) and not isinstance(child, ex.Expander):
                messages.append(
                    ErrorMessage(entry.id, "TestList can only have tests as children")
                )

    return messages


def check_test_statement_id(entry_to_check: en.Entry) -> List[ErrorMessage]:
    """Check rule spec-test-statement-id"""

    all_ids = gather_all_ids(entry_to_check, en.Entry)
    messages: List[ErrorMessage] = []
    for entry in extract_entries_of_type(entry_to_check, en.Test):
        if (
            hasattr(entry, "verify_id")
            and entry.verify_id
            and entry.verify_id not in all_ids
        ):
            messages.append(
                ErrorMessage(
                    entry.id,
                    f"Test refers to an unvalid id: verify_id={entry.verify_id}",
                )
            )

    return messages
