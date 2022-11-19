#! env python3

"""Utilities"""

import yaml


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


class Design(yaml.YAMLObject):
    """Design value object, contains the full design"""
    yaml_loader = yaml.SafeLoader
    yaml_tag = "!Design"

    def __init__(self, definitions, requirements):
        self.definitions = definitions
        self.requirements = requirements


class Requirement(yaml.YAMLObject):
    """Requirement value object"""
    yaml_loader = yaml.SafeLoader
    yaml_tag = "!Requirement"

    def __init__(self, id, text):
        self.id = id
        self.text = text
