"""Unit test for doxygen test extraction"""

import unittest
import subprocess
from pathlib import Path

import misc_util as mu

PY = mu.get_python_executable().as_posix()


class TestDesignUtil(unittest.TestCase):
    """Test"""

    def test_pylint(self) -> None:
        """Test"""
        self.assertEqual(
            mu.run_on_all_git_files(f"{PY} -m pylint", Path("."), ["py"], False), 0
        )

    def test_flake8(self) -> None:
        """Test"""
        ret = subprocess.run(f"{PY} -m flake8 .", check=False)
        self.assertEqual(ret.returncode, 0)

    def test_mypy(self) -> None:
        """Test"""
        ret = subprocess.run(f"{PY} -m mypy .", check=False)
        self.assertEqual(ret.returncode, 0)

    def test_black(self) -> None:
        """Test"""
        ret = subprocess.run(f"{PY} -m black --check .", check=False)
        self.assertEqual(ret.returncode, 0)
