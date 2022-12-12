"""Utilities"""

# needed until python 3.10:
# https://stackoverflow.com/questions/36286894/name-not-defined-in-type-annotation
from __future__ import annotations
from typing import List, Optional
from enum import Enum

import re
import yaml


LINK_EXPRESSION = re.compile("<([a-zA-Z_][a-zA-Z0-9_-]*)>")


class Entry(yaml.YAMLObject):
    """Any entry: this is the parent class for all other. Virtual."""

    short_type = "en"
    yaml_loader = yaml.SafeLoader
    yaml_tag = "!Entry"

    def __init__(self, id1: str, text: str, children: List[Entry]):
        self.id = id1  # pylint: disable=C0103
        self.text = text
        self.children = children

    def get_id(self) -> str:
        """Return the id if applicable else None"""
        return self.id if hasattr(self, "id") and self.id is not None else ""

    def get_text(self) -> str:
        """Return the text if applicable else None"""
        return self.text if hasattr(self, "text") and self.text is not None else ""

    def get_children(self) -> List[Entry]:
        """Return the children if applicable else []"""
        return (
            self.children
            if hasattr(self, "children") and self.children is not None
            else []
        )

    def expand(self, design: Entry, _parent: Optional[Entry]) -> List[Entry]:
        """Processing: Nothing to do by default but call on children"""
        try:
            if self.get_children():
                old_children = self.children
                self.children = []

                for child in old_children:
                    self.children += child.expand(design, self)
            return [self]

        except Exception as exc:
            print(f"Exception while expanding {self.get_id()}:", exc)
            raise

    def print(self, indent: int = 0) -> None:
        """Print to stdout (for debug)"""
        text_str = f", text: {self.get_text()}"
        children_str = f", (nb_children: {len(self.get_children())})"
        print(f"{indent * 2 * ' '}id: {self.id}" + text_str + children_str)

        for child in self.get_children():
            child.print(indent + 1)

    def extract_links(self) -> List[str]:
        """Extract all the links mentioned in the associated text"""
        return LINK_EXPRESSION.findall(self.get_text())

    def simplify(self) -> None:
        """Remove fields that are empty, to simplify writing to YAML"""
        keys_to_delete: List[str] = []
        for attribute_name, _ in self.__dict__:
            if hasattr(self, attribute_name) and not getattr(self, attribute_name):
                keys_to_delete.append(attribute_name)

        for attribute_name in keys_to_delete:
            delattr(self, attribute_name)

        for child in self.get_children():
            child.simplify()


class Section(Entry):
    """A section: only to organize entries"""

    short_type = "se"
    yaml_tag = "!Section"


class Definition(Entry):
    """Definition value object"""

    short_type = "def"
    yaml_tag = "!Definition"


class Statement(Entry):
    """Statement value object"""

    short_type = "sta"
    yaml_tag = "!Statement"


class Requirement(Statement):
    """Requirement value object"""

    short_type = "req"
    yaml_tag = "!Requirement"


class Specification(Statement):
    """Specification value object"""

    short_type = "spec"
    yaml_tag = "!Specification"


class TestType(Enum):
    """The different types of tests"""

    AUTOMATIC = "automatic"
    MANUAL = "manual"
    INSPECTION = "inspection"


class Test(Entry):
    """Test value object"""

    short_type = "test"
    yaml_tag = "!Test"

    def __init__(
        self,
        id1: str,
        text: str,
        type1: TestType,
        verify_id: str,
    ):
        super().__init__(id1, text, [])
        self.type = type1.value
        self.verify_id = verify_id


class TestList(Entry):
    """TestList value object"""

    short_type = "tl"
    yaml_tag = "!TestList"


class Design(Entry):
    """Design value object, contains the full design"""

    short_type = "de"
    yaml_tag = "!Design"
