"""Unit test for doxygen test extraction"""

import io
import unittest
from pathlib import Path

import design_util as du
import yaml_util as yu


class TestDesignUtil(unittest.TestCase):
    """Test"""


    def compare_text_files(self, path1: Path, path2: Path) -> None:
        # with open(io.open(path1.as_posix())) as f1, open(io.open(path2.as_posix())) as f2:
        with io.open(path1.as_posix()) as f1, io.open(path2.as_posix()) as f2:
            self.assertListEqual(list(f1), list(f2))

    def test_creation(self) -> None:
        """Test"""

        # entry = du.Entry("id1", "Some text", None)
        statement = du.Statement("id2", "Some text", None)
        definition = du.Definition("id3", "Some text", None)

        self.assertEqual(statement.id, "id2")

        self.assertEqual(definition.id, "id3")

    def test_include(self) -> None:
        """Test"""

        data_path = Path("test/include")
        entries = yu.read_design(data_path / "input1.yaml")
        for entry in entries:
            entry.expand(None)
        yu.write_design(data_path / "output1.yaml", entries)
        self.compare_text_files(data_path / "expected1.yaml", data_path / "output1.yaml")

    def test_extract_tests_from_doxygen(self) -> None:
        """Test"""

        data_path = Path("test/doxygen_tests")
        entries = yu.read_design(data_path / "input1.yaml")
        for entry in entries:
            entry.expand(None)
        yu.write_design(data_path / "output1.yaml", entries)
        self.compare_text_files(data_path / "expected1.yaml", data_path / "output1.yaml")
