"""Test engine to run Python unittest tests"""

import os
import subprocess
from pathlib import Path
from typing import Dict, Sequence, Tuple

import misc_util as mu
import entries as en
import testing as te


class TestEnginePythonUnitTest(te.TestEngine):
    """Class to run tests in the python unittest framework"""

    short_type = "ten_pu"
    yaml_tag = "!TestEnginePythonUnitTest"

    # TODO: tested ?
    def __init__(self, id1: str, text: str, path: Path, modules: Sequence[str]) -> None:
        super().__init__(id1, text)
        self.path = path
        self.modules = modules

    def get_path(self) -> Path:
        """Return the proper path"""
        return Path(self.path)

    def run_test(self, test: en.Test) -> Tuple[te.TestResult, str, str]:
        """Run a test"""

        def new_env() -> Dict[str,str]:
            env = os.environ.copy()
            python_path = env["PYTHONPATH"] if "PYTHONPATH" in env else ""
            env["PYTHONPATH"] = ":".join(self.modules)
            if python_path:
                env["PYTHONPATH"] += ":" + python_path
            return env

        exe = mu.get_python_executable()
        test_id = test.get_id()
        if not test_id:
            raise Exception("Test id must be defined")
        command = f"{exe} -m unittest {test.id}"
        # TODO: Handle stdout and stderr
        if hasattr(self, "modules") and self.modules:
            completed_process = subprocess.run(
                command, capture_output=True, check=False, cwd=self.get_path(), env=new_env()
            )
        else:
            completed_process = subprocess.run(
                command, capture_output=True, check=False, cwd=self.get_path()
            )
        if completed_process.returncode != 0:
            print(
                f"Test execution of {test_id} ended with code {completed_process.returncode}"
            )
        return (
            te.TestResult.SUCCESS
            if completed_process.returncode == 0
            else te.TestResult.FAILED,
            completed_process.stdout.decode("utf-8"),
            completed_process.stderr.decode("utf-8"),
        )
