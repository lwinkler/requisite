#! env python3

import yaml

class Definition(yaml.YAMLObject):
    yaml_loader = yaml.SafeLoader
    yaml_tag = u'!Definition'

    def __init__(self, name, definition):
       self.name= name
       self.definition= definition

class List(yaml.YAMLObject):
    yaml_loader = yaml.SafeLoader
    yaml_tag = u'!List'

    def __init__(self, name, elements):
       self.name= name
       self.elements= elements

class Design(yaml.YAMLObject):
    yaml_loader = yaml.SafeLoader
    yaml_tag = u'!Design'

    def __init__(self, definitions, requirements):
       self.definitions= definitions
       self.requirements= requirements

class Requirement(yaml.YAMLObject):
    yaml_loader = yaml.SafeLoader
    yaml_tag = u'!Requirement'

    def __init__(self, id, text):
       self.id= id
       self.text= text

