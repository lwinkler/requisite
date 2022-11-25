#! env python3

"""Utilities"""

# needed until python 3.10:
# https://stackoverflow.com/questions/36286894/name-not-defined-in-type-annotation
from __future__ import annotations
from pathlib import Path
from typing import List, Type

import yaml
import doxygen_util as du


def check_is_instance(statement: Statement, parent_class: Type) -> None:
    """Check if the object inherits from type (exception raised)"""

    if not isinstance(statement, parent_class):
        raise Exception(f"{statement.id} is not an instance of {parent_class.__name__}")


def check_are_instances(statements: List[Statement], parent_class: Type) -> None:
    """Check if the objects inherit from type (exception raised)"""
    for statement in statements:
        check_is_instance(statement, parent_class)


class Statement(yaml.YAMLObject):
    """Any statement: this is the parent class for all other. Virtual."""

    yaml_loader = yaml.SafeLoader
    yaml_tag = "!Statement"

    def __init__(self, id1: str, name: str, text: str, children: List[Statement]):
        self.id = id1  # pylint: disable=C0103
        if name is not None:
            self.name = name
        if text is not None:
            self.text = text
        if children is not None:
            self.children = children

    def __str__(self):
        name_str = f", name: {self.name}" if hasattr(self, "name") else ""
        text_str = f", text: {self.text}" if hasattr(self, "text") else ""
        children_str = (
            f", nb_children: {len(self.children)}" if hasattr(self, "children") else ""
        )
        return f"id: {self.id}" + name_str + text_str + children_str


class Definition(Statement):
    """Definition value object"""

    yaml_tag = "!Definition"

    def __init__(self, id1: str, name: str, text: str, children: List[Statement]):
        super().__init__(id1, name, text, children)


class Requirement(Statement):
    """Requirement value object"""

    yaml_tag = "!Requirement"

    def __init__(self, id1: str, name: str, text: str, children: List[Statement]):
        super().__init__(id1, name, text, children)


class Test(Statement):
    """Test value object"""

    yaml_tag = "!Test"

    def __init__(
        self,
        id1: str,
        name: str,
        text: str,
        children: List[Statement],
        requirement: str,
    ):
        super().__init__(id1, name, text, children)
        self.requirement = requirement


class TestList(Statement):
    """TestList value object"""

    yaml_tag = "!TestList"

    def __init__(self, id1: str, name: str, text: str, children: List[Statement]):
        super().__init__(id1, name, text, children)

    def list_tests(self):
        """Generate the list of tests"""
        check_are_instances(self.children, Test)
        return self.children


class TestListFromDoxygen(TestList):
    """TestListFromDoxygen value object: can extract test information from doxygen tags"""

    yaml_tag = "!TestListFromDoxygen"

    def __init__(
        self, id1: str, name: str, text: str, children: List[Statement], path: Path
    ):
        super().__init__(id1, name, text, children)
        self.path = path

    def get_path(self) -> Path:
        """Return a Path object"""
        return Path(self.path)

    def list_tests(self) -> List[Test]:
        """Generate the list of tests"""
        all_functions = du.extract_tests_from_functions(self.get_path())
        return [Test(self.id + "-" + index, func.name, None, None, func.requirement) for index, func in enumerate(all_functions)]


class Design(yaml.YAMLObject):
    """Design value object, contains the full design"""

    yaml_loader = yaml.SafeLoader
    yaml_tag = "!Design"

    def __init__(
        self,
        statements: List[Statement]
    ):
        self.statements = statements

    def list_tests(self):
        """Generate the test list"""
        tests = []
        for list1 in self.statements:
            if isinstance(list1, TestList):
                tests += list1.list_tests()
        return tests
