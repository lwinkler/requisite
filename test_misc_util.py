"""Test for misc util"""

import unittest
import subprocess
from pathlib import Path
from typing import List
import misc_util as mu


class TestMiscUtil(unittest.TestCase):
    """Test"""

    def contain_path(self, paths: List[Path], path_to_search: Path) -> bool:
        """Check if path is contained"""
        for path in paths:
            if path.as_posix() == path_to_search.as_posix():
                return True
        return False

    def test_get_python_executable(self) -> None:
        """Test"""
        exe = mu.get_python_executable()

        self.assertTrue(exe.is_file())
        self.assertTrue("python" in exe.as_posix())

    def test_generate_all_git_files_command(self) -> None:
        """Test"""
        command = mu.generate_all_git_files_command(Path("some/path"), [])
        self.assertEqual(command, "git ls-files some/path")
        command = mu.generate_all_git_files_command(Path("some/path"), ["ext"])
        self.assertEqual(command, 'git ls-files some/path | grep -e "\\.ext$"')
        command = mu.generate_all_git_files_command(Path("some/path"), ["ext", "md"])
        self.assertEqual(
            command, 'git ls-files some/path | grep -e "\\.ext$" -e "\\.md$"'
        )

    def test_list_all_git_files(self) -> None:
        """Test"""
        all_files1 = mu.list_all_git_files(Path("test_data/misc"), [])
        all_files2 = mu.list_all_git_files(Path("."), [])
        all_files3 = mu.list_all_git_files(Path("."), ["myext"])
        all_files4 = mu.list_all_git_files(Path("."), ["py"])

        self.assertTrue(
            self.contain_path(all_files1, Path("test_data/misc/myfile.myext"))
        )
        self.assertTrue(
            self.contain_path(all_files2, Path("test_data/misc/myfile.myext"))
        )
        self.assertTrue(
            self.contain_path(all_files3, Path("test_data/misc/myfile.myext"))
        )
        self.assertFalse(
            self.contain_path(all_files4, Path("test_data/misc/myfile.myext"))
        )

    def test_failing_command(self) -> None:
        """Test"""

        def failing() -> None:
            subprocess.run("false", check=True)

        subprocess.run("false", check=False)
        self.assertRaises(Exception, failing)

    def test_run_on_all_git_files(self) -> None:
        """Execute a command on all files using git and xargs"""

        mu.run_on_all_git_files("echo py files: ", Path("."), ["py"])
        mu.run_on_all_git_files("echo myext files: ", Path("."), ["myext"])
        mu.run_on_all_git_files("echo myext and md files: ", Path("."), ["md"])
        mu.run_on_all_git_files("echo myext and md files: ", Path("."), ["md", "myext"])

        def failing() -> None:
            mu.run_on_all_git_files("false", Path("."), ["myext"])

        self.assertRaises(Exception, failing)
