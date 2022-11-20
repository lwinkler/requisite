#! env python3

"""Utilities"""

import yaml
from pathlib import Path


class Definition(yaml.YAMLObject):
    """Definition value object"""
    yaml_loader = yaml.SafeLoader
    yaml_tag = "!Definition"

    def __init__(self, name, definition):
        self.name = name
        self.definition = definition


class DefinitionList(yaml.YAMLObject):
    """TODO keep"""
    yaml_loader = yaml.SafeLoader
    yaml_tag = "!DefinitionList"

    def __init__(self, name, elements):
        self.name = name
        self.elements = elements


class Requirement(yaml.YAMLObject):
    """Requirement value object"""
    yaml_loader = yaml.SafeLoader
    yaml_tag = "!Requirement"

    def __init__(self, id, text):
        self.id = id
        self.text = text

class Test(yaml.YAMLObject):
    """Test value object"""
    yaml_loader = yaml.SafeLoader
    yaml_tag = "!Test"

    def __init__(self, id, requirement):
        self.id = id
        self.requirement = requirement

class TestList(yaml.YAMLObject):
    """TestList value object"""
    yaml_loader = yaml.SafeLoader
    yaml_tag = "!TestList"

    def __init__(self, name: str, tests: Test):
        self.name = name
        self.tests = tests

    def list_tests(self):
    	return self.tests

class UnitTestList(yaml.YAMLObject):
    """UnitTestList value object"""
    yaml_loader = yaml.SafeLoader
    yaml_tag = "!UnitTestList"

    def __init__(self, name: str, path: Path):
        self.name = name
        self.path = path

    def list_tests(self):
    	return []

class Design(yaml.YAMLObject):
    """Design value object, contains the full design"""
    yaml_loader = yaml.SafeLoader
    yaml_tag = "!Design"

    def __init__(self, definitions, requirements, test_lists):
        self.definitions = definitions
        self.requirements = requirements
        self.test_lists = test_lists

    def list_tests(self):
    	tests = []
    	for l in self.test_lists:
    		tests += l.list_tests()
    	return tests
