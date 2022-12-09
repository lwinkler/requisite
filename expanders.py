"""Expanders are entries that can modify their parent entry (then are removed)"""

from pathlib import Path
from typing import List, Optional

import yaml_util as yu
from entries import Entry


class Expander(Entry):
    """Parent class for all entries that add entries to their parent"""

    yaml_tag = "!Expander"

    def create_entries(self, parent: Entry) -> List[Entry]:
        """Create the entries to be added in the parent's child"""
        raise NotImplementedError()

    def expand(self, parent: Optional[Entry]):
        """Processing: extract child tests"""
        if parent is None:
            raise Exception("Cannot use expanders at top level")
        if hasattr(self, "children"):
            raise Exception("Include children should not be defined manually")
        super().expand(self)
        parent.children.remove(self)
        new_entries = self.create_entries(parent)
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

    def create_entries(self, parent: Entry) -> List[Entry]:
        return yu.read_entries(self.get_path())

    def get_path(self) -> Path:
        """Return a Path object"""
        return Path(self.path)
