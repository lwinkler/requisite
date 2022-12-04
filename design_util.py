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

    def __init__(self, id1: str, text: str, children: List[Entry]):
        self.id = id1  # pylint: disable=C0103
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


class Section(Entry):
    """A section: only to organize entries"""

    yaml_tag = "!Section"


class Expander(Entry):
    """Parent class for all entries that add entries to their parent"""

    yaml_tag = "!Expander"

    def create_entries(self) -> List[Entry]:
        raise NotImplementedError()

    def expand(self, parent: Entry):
        """Processing: extract child tests"""
        if hasattr(self, "children"): # TODO: Remove children
            raise Exception(
                "Include children should not be defined manually"
            )
        super().expand(self)
        parent.children.remove(self)
        new_entries = self.create_entries()
        for entry in new_entries:
            entry.expand(self)
        parent.children += new_entries

class Include(Expander):
    """Placeholder class that expands its parent to include another YAML file"""

    yaml_tag = "!Include"

    def __init__(  # pylint: disable=R0913
        self, id1: str, text: str, children: List[Entry], path: Path
    ):
        super().__init__(id1, text, children)
        self.path = path

    def create_entries(self) -> List[Entry]:
        return read_entries(self.get_path())

    def get_path(self) -> Path:
        """Return a Path object"""
        return Path(self.path)

class ExtractTestsFromDoxygen(Expander):
    """Placeholder class that expands its parent to include another YAML file"""

    yaml_tag = "!ExtractTestsFromDoxygen"

    def __init__(  # pylint: disable=R0913
        self, id1: str, text: str, children: List[Entry], path: Path
    ):
        super().__init__(id1, text, children)
        self.path = path

    def create_entries(self) -> List[Entry]:
        return du.extract_tests_from_functions(self.get_path(), self.id)

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
        text: str,
        children: List[Entry],
        statement: str,
    ):
        super().__init__(id1, text, children)
        self.statement = statement


class TestList(Entry):
    """TestList value object"""

    yaml_tag = "!TestList"

class Design(Entry): # TODO Remove
    """Design value object, contains the full design"""

    yaml_loader = yaml.SafeLoader
    yaml_tag = "!Design"
