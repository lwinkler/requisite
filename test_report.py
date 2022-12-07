"""Unit test for doxygen test extraction"""

import unittest
import yaml

import report as rp


class TestReport(unittest.TestCase):
    """Test operations"""

    def test_text_to_markdown(self):
        """Test"""
        self.assertEqual(
            rp.text_to_markdown("Some simple text with <link>"),
            "Some simple text with [link](#link)",
        )
        self.assertEqual(
            rp.text_to_markdown("<Another> <more_annoying-text> with <link>"),
            "[Another](#Another) [more_annoying-text](#more_annoying-text) with [link](#link)",
        )
        self.assertEqual(
            rp.text_to_markdown("< Another > <more_annoying-text> with <link>"),
            "&lt; Another &gt; [more_annoying-text](#more_annoying-text) with [link](#link)",
        )
