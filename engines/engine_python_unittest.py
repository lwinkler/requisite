"""Test engine to run Python unittest tests"""

import subprocess

import misc_util as mu
import entries as en
import testing as te


class TestEnginePythonUnitTest(te.TestEngine):
    """Class to run tests in the python unittest framework"""

    short_type = "ten_pu"
    yaml_tag = "!TestEnginePythonUnitTest"

    def run_test(self, test: en.Test) -> te.TestResult:
        """Run a test"""

        exe = mu.get_python_executable()
        test_id = test.get_id()
        if not test_id:
            raise Exception("Test id must be defined")
        command = f"{exe} -m unittest {test.id}"
        # TODO: Handle stdout and stderr
        completed_process = subprocess.run(command, capture_output=True, check=False)
        if completed_process.returncode == 0:
            return te.TestResult.PASSED
        print(
            f"Test execution of {test_id} ended with code {completed_process.returncode}"
        )
        return te.TestResult.FAILED
