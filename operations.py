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
    level: str
    message: str


def extract_entries_of_type(entry: en.Entry, parent_class: Type) -> List[en.Entry]:
    """Extract all instances that inherit from the type"""

    res: List[en.Entry] = []

    if isinstance(entry, parent_class):
        res.append(entry)

    if hasattr(entry, "children"):
        for child in entry.children:
            res += extract_entries_of_type(child, parent_class)

    return res

def check_definition_id_mandatory(entry: en.Entry) -> List[ErrorMessage]:
    """Check rule spec-definition-id-mandatory"""
    
    messages: List[ErrorMessage] = []
    for entry in extract_entries_of_type(entry, en.Definition):
        if not hasattr(entry, "id") or entry.id is None or not entry.id:
            messages.append(ErrorMessage("", "Id missing"))
    return messages

# - !Specification
  # id: spec-statement-id-mandatory
  # text: Any *statement must have an id.
# 
# - !Specification
  # id: spec-unique-id
  # text: The id field of any *entry must be unique.
# 
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
