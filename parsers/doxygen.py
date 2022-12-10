"""Utilities for doxygen test parsing"""

import subprocess
import tempfile
import shutil
import xml.etree.ElementTree as ET

from typing import List
from pathlib import Path
from dataclasses import dataclass
import entries as en
import expanders as ex


@dataclass
class Function:
    """A function and the associated statement"""

    name: str
    verify_id: str
    file: Path
    line: int


def function_to_id(path: Path, name: str) -> str:
    """Convert a function name to id"""
    return path.as_posix().replace("/", "-").replace(".", "-") + "-" + name


def extract_tests_from_functions(path: Path) -> List[en.Entry]:
    """Parse the source code to extract the test information"""

    def get_all_xml_files(xml_dir: Path) -> List[Path]:
        res = []
        for path in xml_dir.iterdir():
            if path.as_posix().endswith(".xml") and not path.as_posix().endswith(
                "index.xml"
            ):
                res.append(path)
        res.sort()
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
        statement = get_requirement_node(node)

        return Function(
            name.text,
            statement.text.strip()
            if statement is not None and statement.text
            else None,
            Path(location.attrib["file"]),
            location.attrib["line"],
        )

    def execute(command: List[str], tmp_dir: Path) -> None:
        ret = subprocess.run(
            command,
            cwd=tmp_dir.as_posix(),
            check=True,
            capture_output=True,
            encoding="utf-8",
        )
        # print(ret.stdout)
        if ret.stderr:
            print("Warnings from doxygen documentation generation:")
            print(ret.stderr)
        if ret.returncode != 0:
            raise Exception(f"Command '{command}' failed with code {ret.returncode}")

    def extract_all_functions(xml_file: Path) -> List[Function]:

        tree = ET.parse(xml_file)
        root = tree.getroot()
        res: List[Function] = []
        # print(xml_file.as_posix())
        for memberdef in root.iter("memberdef"):
            if memberdef.attrib["kind"] == "function":
                funct = extract_function(memberdef)

                # only the functions associated with a statement
                if funct.verify_id:
                    res.append(funct)
        return res

    if not path.is_dir():
        raise Exception(f"Directory not found: {path.as_posix()}")
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
INPUT = {path.resolve().as_posix()}
HAVE_DOT = NO
ALIASES = \"verify=@xrefitem verify \\\"Verify\\\" \\\"Verify\\\" \"
"""
            )

        execute(["doxygen", doxyfile.as_posix()], tmp_dir)

        xml_dir = Path(tmp_dir / "xml")
        all_files = get_all_xml_files(xml_dir)

        all_functions = []
        for file in all_files:
            all_functions += extract_all_functions(file)

        return [
            en.Test(
                function_to_id(func.file.relative_to(path.resolve()), func.name),
                "",
                en.TestType.AUTOMATIC,
                func.verify_id,
            )
            for func in all_functions
        ]

    finally:
        print("Delete " + tmp_dir.as_posix())
        shutil.rmtree(tmp_dir)


class ExtractTestsFromDoxygen(ex.Expander):
    """Extract tests from doxygen documentation, C++ or other.
    Will generate XML with doxygen then parse the XML to retrieve the test functions"""

    yaml_tag = "!ExtractTestsFromDoxygen"

    def __init__(  # pylint: disable=R0913
        self, id1: str, text: str, children: List[en.Entry], path: Path
    ):
        super().__init__(id1, text, children)
        self.path = path

    def create_entries(self, parent: en.Entry) -> List[en.Entry]:
        return extract_tests_from_functions(self.get_path())

    def get_path(self) -> Path:
        """Return a Path object"""
        return Path(self.path)
