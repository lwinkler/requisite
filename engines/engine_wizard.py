"""Test engine to run tests manually through a wizard"""

import entries as en
import testing as te
from typing import Tuple


class TestEngineWizard(te.TestEngine):
    """Class to run tests in the python unittest framework"""

    short_type = "ten_w"
    yaml_tag = "!TestEngineWizard"

    def run_test(self, test: en.Test) -> Tuple[te.TestResult, str, str]:
        """Run a test"""
        # TODO
        return te.TestResult.SKIPPED, "", ""
