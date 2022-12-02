"""Unit test for doxygen test extraction"""

import unittest
import subprocess
from pathlib import Path

import misc_util as mu

PY = mu.get_python_executable().as_posix()


class TestDesignUtil(unittest.TestCase):
    """Test"""

    def test_pylint(self):
        """Test"""
        mu.run_on_all_git_files(f"{PY} -m pylint", Path("."), ["py"])

    def test_flake8(self):
        """Test"""
        ret = subprocess.run(f"{PY} -m flake8 .", check=True)
        self.assertEqual(ret.returncode, 0)

    def test_mypy(self):
        """Test"""
        ret = subprocess.run(f"{PY} -m mypy .", check=True)
        self.assertEqual(ret.returncode, 0)

    def test_black(self):
        """Test"""
        ret = subprocess.run(f"{PY} -m black --check .", check=True)
        self.assertEqual(ret.returncode, 0)
