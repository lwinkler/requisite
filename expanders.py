"""Expanders are entries that can modify their parent entry (then are removed)"""

import copy
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

    def expand(self, parent: Optional[Entry]) -> List[Entry]:
        """Processing: extract child tests"""
        if parent is None:
            raise Exception("Cannot use expanders at top level")

        results = self.create_entries(parent) # TODO
        for result in results:
            result.expand(parent)
        return results

        results : List[Entry] = []
        new_entries = [self]
        while new_entries:
            for entry in new_entries:
                new_entries2 = self.create_entries(parent)


        return results


class Include(Expander):
    """Placeholder class that expands its parent to include another YAML file"""

    yaml_tag = "!Include"

    def __init__(  # pylint: disable=R0913
        self, id1: str, text: str, path: Path
    ):
        super().__init__(id1, text, [])
        self.path = path

    def create_entries(self, parent: Entry) -> List[Entry]:
        return yu.read_entries(self.get_path())

    def get_path(self) -> Path:
        """Return a Path object"""
        return Path(self.path)

class MultiplyByDefinition(Expander):
    """Placeholder class that expands its parent to include another YAML file"""

    yaml_tag = "!MultiplyByDefinition"

    def __init__(  # pylint: disable=R0913
            self, id1: str, text: str, definition_id: str
    ):
        super().__init__(id1, text, [])
        self.definition_id = definition_id

    def create_entries(self, parent: Entry) -> List[Entry]:
        ret: List[Entry] = []
        ttt = ["a", "b", "cTODO"]
        for t in ttt:
            ret.append(copy.deepcopy(parent))
            last = ret[-1]
            last.id += "-" + t
            if hasattr(last, "text"):
                last.text += f" ({t})"
            last.children = copy.deepcopy(self.get_children())
            print(444, len(parent.get_children()), len(last.get_children()))

        return ret
