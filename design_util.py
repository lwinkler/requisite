#! env python3

"""Utilities"""

import yaml
from pathlib import Path
from typing import List

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

import subprocess
# import tempfile
import xml.etree.ElementTree as ET

class DoxygenTestList(yaml.YAMLObject):
    """DoxygenTestList value object: can extract test information from doxygen tags"""
    yaml_loader = yaml.SafeLoader
    yaml_tag = "!DoxygenTestList"

    def __init__(self, name: str, path: Path):
        self.name = name
        self.path = path

    def list_tests(self):
        # tmpdir = tempfile.TemporaryDirectory()

        def get_all_xml_files(xml_dir: Path) -> List[Path]:
            res = []
            for p in xml_dir.iterdir():
                if p.as_posix().endswith(".xml"):
                    res.append(p)
            return res

        def get_function_name(node) -> str:
            res = []
            for name in node.iter("name"):
                res.append(name.text)
            assert(len(res) == 1)
            return res[0]

        def get_all_functions(xml_file: Path):
            tree = ET.parse(xml_file)
            root = tree.getroot()
            res = []
            print(xml_file.as_posix())
            for memberdef in root.iter("memberdef"):
                if memberdef.attrib["kind"] == "function":
                    name = get_function_name(memberdef)
                    for descr in memberdef.iter("detaileddescription"):
                        for para1 in descr.iter("para"):
                            print(888, para1.attrib, para1.text)
                            for xrefsect in para1.iter("xrefsect"):
                                print(999)
                                for xrefdescription in xrefsect.iter("xrefdescription"):
                                    print(9991)
                                    for para2 in xrefdescription.iter("para"):
                                        print(666, name, paraw)
                                        res.append(Path(name.text))
            return res

        command = ["doxygen", "Doxyfile", self.path.as_posix()]
        xml_dir = Path("xml")
        subprocess.run(command)
        all_files = get_all_xml_files(xml_dir)

        all_functions = []
        for f in all_files:
            all_functions += get_all_functions(f)

        print(all_functions)

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
