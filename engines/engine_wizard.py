"""Test engine to run tests manually through a wizard"""

import misc_util as mu
import entries as en
import testing as te

class TestEngineWizard(te.TestEngine):
    """Class to run tests in the python unittest framework"""
    short_type = "ten_w"
    yaml_tag = "!TestEngineWizard"


    def run_test(self, test: en.Test) -> te.TestResult:
        """Run a test"""
        # TODO
        return te.TestResult.SKIPPED
