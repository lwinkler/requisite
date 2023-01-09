"""Unit test for doxygen test extraction"""

import os
import unittest
import subprocess
from pathlib import Path
from typing import Dict

import misc_util as mu

PY = mu.get_python_executable().as_posix()
print("Python path:", PY)

EXCLUDED_PATHS = [Path(".git"), Path(".mypy_cache"), Path("__pycache__")]


def prepend_to_env(variable_name: str, value: str) -> Dict[str, str]:
    """Create a new environment with a modified variable"""
    env = os.environ.copy()
    old_value = env[variable_name] if variable_name in env else ""
    env[variable_name] = value
    if old_value:
        env[variable_name] += ":" + old_value
    return env


class TestLint(unittest.TestCase):
    """Test"""

    def test_spec_code_check_pylint(self) -> None:
        """Test"""
        self.assertEqual(
            mu.run_on_all_files(
                f"{PY} -m pylint",
                Path(".."),
                ["py"],
                EXCLUDED_PATHS,
                False,
                env=prepend_to_env("PYTHONPATH", "../src/requisite"),
            ),
            0,
        )

    def test_spec_code_check_flake8(self) -> None:
        """Test"""
        ret = subprocess.run(f"{PY} -m flake8 .", check=False)
        self.assertEqual(ret.returncode, 0)

    def test_spec_code_check_mypy_src(self) -> None:
        """Test"""
        # TODO test once
        ret = subprocess.run(
            f"{PY} -m mypy src",
            cwd="..",
            check=False,
            env=prepend_to_env("MYPYPATH", "../src/requisite"),
        )
        self.assertEqual(ret.returncode, 0)

    def test_spec_code_check_mypy_tests(self) -> None:
        """Test"""
        ret = subprocess.run(
            f"{PY} -m mypy .",
            check=False,
            env=prepend_to_env("MYPYPATH", "../src/requisite"),
        )
        self.assertEqual(ret.returncode, 0)

    def test_spec_code_check_black(self) -> None:
        """Test"""
        ret = subprocess.run(f"{PY} -m black --check .", check=False)
        self.assertEqual(ret.returncode, 0)
