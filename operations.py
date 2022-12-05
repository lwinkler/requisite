"""Operations on design and entries"""

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
    """Check rule spec-statement-id-mandatory"""
    
    known_ids: List[str] = []
    messages: List[ErrorMessage] = []

    for entry in extract_entries_of_type(entry, en.Entry):
        if hasattr(entry, "id") and entry.id is not None and entry.id:
            if entry.id in known_ids:
                messages.append(ErrorMessage(entry.id, "ID is duplicated"))
            else:
                known_ids.append(entry.id)
    return messages

# - !Specification
  # id: spec-id-valid-chars
# 
# - !Specification
  # id: spec-id-spec
  # text: The id field of any *specification must be start with spec.
# 
# - !Specification
  # id: spec-id-spec
  # text: The id field of any *specification must be start with req.
# 
# - !Specification
  # id: spec-valid-links
  # text: The links in any text field of any *entry must be an existing entry id.
