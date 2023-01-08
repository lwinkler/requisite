"""Test engine to run Python unittest tests"""

import subprocess

import misc_util as mu
import entries as en
import testing as te
from typing import Tuple


class TestEnginePythonUnitTest(te.TestEngine):
    """Class to run tests in the python unittest framework"""

    short_type = "ten_pu"
    yaml_tag = "!TestEnginePythonUnitTest"

    def run_test(self, test: en.Test) -> Tuple[te.TestResult, str, str]:
        """Run a test"""

        exe = mu.get_python_executable()
        test_id = test.get_id()
        if not test_id:
            raise Exception("Test id must be defined")
        command = f"{exe} -m unittest {test.id}"
        # TODO: Handle stdout and stderr
        completed_process = subprocess.run(command, capture_output=True, check=False)
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
