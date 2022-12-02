"""Utilities for doxygen test parsing"""

import subprocess
import tempfile
import shutil
import xml.etree.ElementTree as ET

from typing import List
from pathlib import Path
from dataclasses import dataclass
import design_util as du


@dataclass
class Function:
    """A function and the associated statement"""

    name: str
    statement: str
    file: Path
    line: int


def extract_tests_from_functions(path: Path, test_list_id: str) -> List[Function]:
    """Parse the source code to extract the test information"""

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
        statement = get_requirement_node(node)

        if statement is not None and statement.text:
            return Function(
                name.text,
                statement.text.strip(),
                location.attrib["file"],
                location.attrib["line"],
            )
        return Function(name.text, "", location.attrib["file"], location.attrib["line"])

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
                if funct.statement:
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

        command = ["doxygen", doxyfile.as_posix()]
        execute(command, tmp_dir)

        xml_dir = Path(tmp_dir / "xml")
        all_files = get_all_xml_files(xml_dir)

        all_functions = []
        for file in all_files:
            all_functions += extract_all_functions(file)

        all_tests = [
            du.Test(f"{test_list_id}-{index}", func.name, None, None, func.statement)
            for index, func in enumerate(all_functions)
        ]

        return all_tests

    finally:
        print("Delete " + tmp_dir.as_posix())
        shutil.rmtree(tmp_dir)
