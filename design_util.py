"""Utilities"""

# needed until python 3.10:
# https://stackoverflow.com/questions/36286894/name-not-defined-in-type-annotation
from __future__ import annotations
from pathlib import Path
from typing import List

import yaml
import doxygen_util as du

def read_entries(path: Path) -> List[du.Entry]:
    """Read a list of entries in YAML format"""
    with open(path, encoding="utf-8") as fin:
        return yaml.safe_load(fin.read())

class Entry(yaml.YAMLObject):
    """Any entry: this is the parent class for all other. Virtual."""

    yaml_loader = yaml.SafeLoader
    yaml_tag = "!Entry"

    def __init__(self, id1: str, name: str, text: str, children: List[Entry]):
        self.id = id1  # pylint: disable=C0103
        if name is not None:
            self.name = name
        if text is not None:
            self.text = text
        if children is not None:
            self.children = children

    def expand(self, parent: Entry):
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
        name_str = f", name: {self.name}" if hasattr(self, "name") else ""
        text_str = f", text: {self.text}" if hasattr(self, "text") else ""
        children_str = (
            f", (nb_children: {len(self.children)})"
            if hasattr(self, "children")
            else ""
        )
        print(f"{indent * 2 * ' '}id: {self.id}" + name_str + text_str + children_str)

        if hasattr(self, "children"):
            for child in self.children:
                child.print(indent + 1)


class Section(Entry):
    """A section: only to organize entries"""

    yaml_tag = "!Section"


class Include(Entry):
    """Placeholder class that expands its parent to include another YAML file"""

    yaml_tag = "!Include"

    def __init__(  # pylint: disable=R0913
        self, id1: str, name: str, text: str, children: List[Entry], path: Path
    ):
        super().__init__(id1, name, text, children)
        self.path = path

    def expand(self, parent: Entry):
        """Processing: extract child tests"""
        if hasattr(self, "children"): # TODO: Remove children
            raise Exception(
                "Include children should not be defined manually"
            )
        parent.children.remove(self)
        parent.children += read_entries(self.get_path())
        # super().expand(self)

    def get_path(self) -> Path:
        """Return a Path object"""
        return Path(self.path)


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
        name: str,
        text: str,
        children: List[Entry],
        statement: str,
    ):
        super().__init__(id1, name, text, children)
        self.statement = statement


class TestList(Entry):
    """TestList value object"""

    yaml_tag = "!TestList"


class TestListFromDoxygen(TestList):
    """TestListFromDoxygen value object:
    can extract test information from doxygen tags"""

    yaml_tag = "!TestListFromDoxygen"

    def __init__(  # pylint: disable=R0913
        self, id1: str, name: str, text: str, children: List[Entry], path: Path
    ):
        super().__init__(id1, name, text, children)
        self.path = path

    def expand(self, parent: Entry):
        """Processing: extract child tests"""
        if hasattr(self, "children"):
            raise Exception(
                "TestListFromDoxygen children should not be defined manually"
            )
        self.children = du.extract_tests_from_functions(self.get_path(), self.id)
        super().expand(self)

    def get_path(self) -> Path:
        """Return a Path object"""
        return Path(self.path)


class Design(Entry):
    """Design value object, contains the full design"""

    yaml_loader = yaml.SafeLoader
    yaml_tag = "!Design"
