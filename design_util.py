#! env python3

"""Utilities"""

from pathlib import Path
from typing import List

import yaml
import doxygen_util as du


class Definition(yaml.YAMLObject):
    """Definition value object"""

    yaml_loader = yaml.SafeLoader
    yaml_tag = "!Definition"

    def __init__(self, name, text: str):
        self.name = name
        self.text = text


class DefinitionList(yaml.YAMLObject):
    """TODO keep"""

    yaml_loader = yaml.SafeLoader
    yaml_tag = "!DefinitionList"

    def __init__(self, name: str, elements: List[Definition]):
        self.name = name
        self.elements = elements


class Requirement(yaml.YAMLObject):
    """Requirement value object"""

    yaml_loader = yaml.SafeLoader
    yaml_tag = "!Requirement"

    def __init__(self, id1: str, text: str):
        self.id = id1 # pylint: disable=C0103
        self.text = text


class Test(yaml.YAMLObject):
    """Test value object"""

    yaml_loader = yaml.SafeLoader
    yaml_tag = "!Test"

    def __init__(self, id1: str, requirement: str):
        self.id = id1 # pylint: disable=C0103
        self.requirement = requirement


class TestList(yaml.YAMLObject):
    """TestList value object"""

    yaml_loader = yaml.SafeLoader
    yaml_tag = "!TestList"

    def __init__(self, name: str, tests: Test):
        self.name = name
        self.tests = tests

    def list_tests(self):
        """Generate the list of tests"""
        return self.tests


class TestListFromDoxygen(yaml.YAMLObject):
    """TestListFromDoxygen value object: can extract test information from doxygen tags"""

    yaml_loader = yaml.SafeLoader
    yaml_tag = "!TestListFromDoxygen"

    def __init__(self, name: str, path: str):
        self.name = name
        self.path = path

    def get_path(self) -> Path:
        """Return a Path object"""
        return Path(self.path)

    def list_tests(self) -> List[Test]:
        """Generate the list of tests"""
        all_functions = du.extract_tests_from_functions(self.get_path())
        return [Test(func.name, func.requirement) for func in all_functions]


class Design(yaml.YAMLObject):
    """Design value object, contains the full design"""

    yaml_loader = yaml.SafeLoader
    yaml_tag = "!Design"

    def __init__(self, definitions: List[Definition], requirements: List[Requirement], test_lists: List[TestList]):
        self.definitions = definitions
        self.requirements = requirements
        self.test_lists = test_lists

    def list_tests(self):
        """Generate the test list"""
        tests = []
        for list1 in self.test_lists:
            tests += list1.list_tests()
        return tests
