"""Utilities"""

# needed until python 3.10:
# https://stackoverflow.com/questions/36286894/name-not-defined-in-type-annotation
from __future__ import annotations
from typing import List

import re
import yaml


class Entry(yaml.YAMLObject):
    """Any entry: this is the parent class for all other. Virtual."""

    yaml_loader = yaml.SafeLoader
    yaml_tag = "!Entry"

    def __init__(self, id1: str, text: str, children: List[Entry]):
        self.id = id1  # pylint: disable=C0103
        if text is not None:
            self.text = text
        if children is not None:
            self.children = children

    def expand(self, _parent: Entry):
        """Processing: Nothing to do by default but call on children"""
        try:
            if hasattr(self, "children"):
                for child in self.children:
                    child.expand(self)
        except Exception as exc:
            print(f"Exception while expanding {self.id}:", exc)
            raise

    def print(self, indent: int = 0) -> None:
        """Print to stdout (for debug)"""
        text_str = f", text: {self.text}" if hasattr(self, "text") else ""
        children_str = (
            f", (nb_children: {len(self.children)})"
            if hasattr(self, "children")
            else ""
        )
        print(f"{indent * 2 * ' '}id: {self.id}" + text_str + children_str)

        if hasattr(self, "children"):
            for child in self.children:
                child.print(indent + 1)

    def extract_links(self) -> List[str]:
        """Extract all the links mentioned in the associated text"""
        expression = re.compile("<([a-zA-Z_][a-zA-Z0-9_-]*)>")
        results = expression.findall(self.text)
        if not results:
            return []
        return [result for result in results]


class Section(Entry):
    """A section: only to organize entries"""

    yaml_tag = "!Section"


class Definition(Entry):
    """Definition value object"""

    yaml_tag = "!Definition"


class Statement(Entry):
    """Statement value object"""

    yaml_tag = "!Statement"


class Requirement(Statement):
    """Requirement value object"""

    yaml_tag = "!Requirement"


class Specification(Statement):
    """Specification value object"""

    yaml_tag = "!Specification"


class Test(Entry):
    """Test value object"""

    yaml_tag = "!Test"

    def __init__(  # pylint: disable=R0913
        self,
        id1: str,
        text: str,
        children: List[Entry],
        statement: str,
    ):
        super().__init__(id1, text, children)
        self.statement = statement


class TestList(Entry):
    """TestList value object"""

    yaml_tag = "!TestList"


class Design(Entry):
    """Design value object, contains the full design"""

    yaml_loader = yaml.SafeLoader
    yaml_tag = "!Design"
