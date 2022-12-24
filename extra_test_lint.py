"""Unit test for doxygen test extraction"""

import unittest
import subprocess
from pathlib import Path

import misc_util as mu

PY = mu.get_python_executable().as_posix()

EXCLUDED_PATHS = [Path(".git"), Path(".mypy_cache"), Path("__pycache__")]

class TestDesignUtil(unittest.TestCase):
    """Test"""

    def test_spec_code_check_pylint(self) -> None:
        """Test"""
        self.assertEqual(
            mu.run_on_all_files(f"{PY} -m pylint", Path("."), ["py"], EXCLUDED_PATHS, False), 0
        )

    def test_spec_code_check_flake8(self) -> None:
        """Test"""
        ret = subprocess.run(f"{PY} -m flake8 .", check=False)
        self.assertEqual(ret.returncode, 0)

    def test_spec_code_check_mypy(self) -> None:
        """Test"""
        ret = subprocess.run(f"{PY} -m mypy .", check=False)
        self.assertEqual(ret.returncode, 0)

    def test_spec_code_check_black(self) -> None:
        """Test"""
        ret = subprocess.run(f"{PY} -m black --check .", check=False)
        self.assertEqual(ret.returncode, 0)
