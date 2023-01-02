"""Test engine to run Python unittest tests"""

import subprocess

import misc_util as mu
import entries as en
import testing as te


class TestEnginePythonUnittest(te.TestEngine):
    def run_test(self, test: en.Test) -> te.TestExecutionResult:
        exe = mu.get_python_executable()
        test_id = test.get_id()
        if not test_id:
            raise Exception(f"Test id must be defined")
        command = f"{exe} -m unittest {test.id}"
        subprocess.run(command)
        return te.TestExecutionResult.SKIPPED # TODO
