#! env python3

"""Utilities"""

# needed until python 3.10:
# https://stackoverflow.com/questions/36286894/name-not-defined-in-type-annotation
from __future__ import annotations
from pathlib import Path
from typing import List, Type

import yaml
import doxygen_util as du


def check_is_instance(entry: Entry, parent_class: Type) -> None:
    """Check if the object inherits from type (exception raised)"""

    if not isinstance(entry, parent_class):
        raise Exception(f"{entry.id} is not an instance of {parent_class.__name__}")


def check_are_instances(entries: List[Entry], parent_class: Type) -> None:
    """Check if the objects inherit from type (exception raised)"""
    for entry in entries:
        check_is_instance(entry, parent_class)


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

    def expand(self):
        """Processing: Nothing to do by default but call on children"""
        try:
            if hasattr(self, "children"):
                for child in self.children:
                    child.expand()
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

class ExternalSection(Entry):
    """An external section: defined in another YAML file"""

    yaml_tag = "!ExternalSection"

    # def __init__(self, id1: str, name: str, text: str, children: List[Entry]):
        # super().__init__(id1, name, text, children)


class Definition(Entry):
    """Definition value object"""

    yaml_tag = "!Definition"


class Statement(Entry):
    """Statement value object"""

    yaml_tag = "!Statement"


class Test(Entry):
    """Test value object"""

    yaml_tag = "!Test"

    def __init__(
        self,
        id1: str,
        name: str,
        text: str,
        children: List[Entry],
        statement: str,
    ):
        super().__init__(id1, name, text, children)
        self.statement = statement


class TestList(Entry):  # TODO Remove ??
    """TestList value object"""

    yaml_tag = "!TestList"

    def __init__(self, id1: str, name: str, text: str, children: List[Entry]):
        super().__init__(id1, name, text, children)

    def list_tests(self):
        """Generate the list of tests"""
        check_are_instances(self.children, Test)
        return self.children


class TestListFromDoxygen(TestList):
    """TestListFromDoxygen value object: can extract test information from doxygen tags"""

    yaml_tag = "!TestListFromDoxygen"

    def __init__(
        self, id1: str, name: str, text: str, children: List[Entry], path: Path
    ):
        super().__init__(id1, name, text, children)
        self.path = path

    def expand(self):
        """Processing: extract child tests"""
        if hasattr(self, "children"):
            raise Exception(
                "TestListFromDoxygen children should not be defined manually"
            )
        all_functions = du.extract_tests_from_functions(self.get_path())
        self.children = [
            Test(f"{self.id}-{index}", func.name, None, None, func.statement)
            for index, func in enumerate(all_functions)
        ]
        super().expand()

    def get_path(self) -> Path:
        """Return a Path object"""
        return Path(self.path)


class Design(Entry):
    """Design value object, contains the full design"""

    yaml_loader = yaml.SafeLoader
    yaml_tag = "!Design"

    def list_tests(self):
        """Generate the test list"""
        tests = []
        for list1 in self.children:
            if isinstance(list1, TestList):
                tests += list1.list_tests()
        return tests
