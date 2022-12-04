from pathlib import Path
from typing import List

import yaml
import yaml_util as yu
import doxygen_util as du
from design_util import Entry

class Expander(Entry):
    """Parent class for all entries that add entries to their parent"""

    yaml_tag = "!Expander"

    def create_entries(self) -> List[Entry]:
        raise NotImplementedError()

    def expand(self, parent: Entry):
        """Processing: extract child tests"""
        if hasattr(self, "children"): # TODO: Remove children
            raise Exception(
                "Include children should not be defined manually"
            )
        super().expand(self)
        parent.children.remove(self)
        new_entries = self.create_entries()
        for entry in new_entries:
            entry.expand(self)
        parent.children += new_entries

class Include(Expander):
    """Placeholder class that expands its parent to include another YAML file"""

    yaml_tag = "!Include"

    def __init__(  # pylint: disable=R0913
        self, id1: str, text: str, children: List[Entry], path: Path
    ):
        super().__init__(id1, text, children)
        self.path = path

    def create_entries(self) -> List[Entry]:
        return yu.read_entries(self.get_path())

    def get_path(self) -> Path:
        """Return a Path object"""
        return Path(self.path)

class ExtractTestsFromDoxygen(Expander):
    """Placeholder class that expands its parent to include another YAML file"""

    yaml_tag = "!ExtractTestsFromDoxygen"

    def __init__(  # pylint: disable=R0913
        self, id1: str, text: str, children: List[Entry], path: Path
    ):
        super().__init__(id1, text, children)
        self.path = path

    def create_entries(self) -> List[Entry]:
        return du.extract_tests_from_functions(self.get_path(), self.id)

    def get_path(self) -> Path:
        """Return a Path object"""
        return Path(self.path)
