#! env python3

"""Utilities"""

from pathlib import Path
from typing import List

import yaml


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


import subprocess
import tempfile
import shutil
import xml.etree.ElementTree as ET


class Function(yaml.YAMLObject):
    """A function and the associated requirement"""

    def __init__(self, name: str, requirement: str, file: Path, line: int):
        self.name = name
        self.requirement = requirement
        self.file = file
        self.line = line


class DoxygenTestList(yaml.YAMLObject):
    """DoxygenTestList value object: can extract test information from doxygen tags"""

    yaml_loader = yaml.SafeLoader
    yaml_tag = "!DoxygenTestList"

    def __init__(self, name: str, path: str):
        self.name = name
        self.path = path
    
    def get_path(self) -> Path:
        return Path(self.path)

    def list_tests(self):
        """Generate the list of tests"""

        def get_all_xml_files(xml_dir: Path) -> List[Path]:
            res = []
            for path in xml_dir.iterdir():
                if path.as_posix().endswith(".xml") and not path.as_posix().endswith(
                    "index.xml"
                ):
                    res.append(path)
            return res

        def get_child(node, attribute_name: str, check_unique: bool):
            children = []
            for child in node.iter(attribute_name):
                children.append(child)
            if check_unique:
                assert len(children) == 1
            return children[0] if children else None

        def get_requirement_node(node):
            descr = get_child(node, "detaileddescription", True)
            xrefsect = get_child(descr, "xrefsect", False)
            if xrefsect is None:
                return None
            xrefdescr = get_child(xrefsect, "xrefdescription", True)
            return get_child(xrefdescr, "para", False)

        def extract_function(node) -> Function:
            """Extract function from xml node"""

            name = get_child(node, "name", True)
            location = get_child(node, "location", True)
            requirement = get_requirement_node(node)

            if requirement is not None and requirement.text:
                return Function(
                    name.text,
                    requirement.text.strip(),
                    location.attrib["file"],
                    location.attrib["line"],
                )
            return Function(
                name.text, "", location.attrib["file"], location.attrib["line"]
            )

        def extract_all_functions(xml_file: Path) -> List[Function]:
            tree = ET.parse(xml_file)
            root = tree.getroot()
            res: List[Function] = []
            # print(xml_file.as_posix())
            for memberdef in root.iter("memberdef"):
                if memberdef.attrib["kind"] == "function":
                    funct = extract_function(memberdef)

                    # only the functions associated with a requirement
                    if funct.requirement:
                        res.append(funct)
            return res

        tmp_dir = Path(tempfile.mkdtemp("reqdoxy"))
        try:
            doxyfile = tmp_dir / "Doxyfile"
            with open(doxyfile, "w", encoding="utf-8") as fout:
                fout.write(
                    f"""GENERATE_LATEX = NO
GENERATE_HTML = NO
GENERATE_XML = YES
GENERATE_TESTLIST = YES
# OUTPUT_DIRECTORY = {tmp_dir.as_posix()}
RECURSIVE = YES
INPUT = {self.get_path().resolve().as_posix()}
ALIASES =
ALIASES += \"req=@xrefitem req \\\"Requirement\\\" \\\"Requirements\\\" \"
"""
                )

            command = ["doxygen", doxyfile.as_posix()]
            subprocess.run(command, cwd=tmp_dir.as_posix(), check=True)

            xml_dir = Path(tmp_dir / "xml")
            all_files = get_all_xml_files(xml_dir)

            all_functions = []
            for file in all_files:
                all_functions += extract_all_functions(file)

            return all_functions

        finally:
            print("Delete " + tmp_dir.as_posix())
            shutil.rmtree(tmp_dir)


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
