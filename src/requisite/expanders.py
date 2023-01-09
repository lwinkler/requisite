"""Expanders are entries that can modify their parent entry (then are removed)"""

import copy
from pathlib import Path
from typing import Optional

import yaml_util as yu
import operations as op
from entries import Entry, Definition


class Expander(Entry):
    """Parent class for all entries that add entries to their parent"""

    yaml_tag = "!Expander"

    def create_entries(self, design: Entry, parent: Entry) -> list[Entry]:
        """Create the entries to be added in the parent's child"""
        raise NotImplementedError()

    def expand(self, design: Entry, parent: Optional[Entry]) -> list[Entry]:
        """Processing: extract child tests"""
        if parent is None:
            raise Exception("Cannot use expanders at top level")

        results = self.create_entries(design, parent)
        for result in results:
            result.expand(design, parent)
        if len(results) == 0:
            raise Exception(
                f"Expander with id '{self.get_id()}' of type {type(self).__name__}"
                " could not extract any element."
            )
        return results


class Include(Expander):
    """Placeholder class that expands its parent to include another YAML file"""

    yaml_tag = "!Include"

    def __init__(self, id1: str, text: str, path: Path):  # pylint: disable=R0913
        super().__init__(id1, text, [])
        self.path = path

    def get_path(self, design_path) -> Path:
        """Return the path attribute. Since it is relative we need the design_path as well"""
        return design_path.parent / self.path

    def create_entries(self, design: Entry, parent: Entry) -> list[Entry]:
        return yu.read_objects(Entry, self.get_path(design.get_file_path()))


class MultiplyByDefinition(Expander):
    """Placeholder class that expands its parent to include another YAML file"""

    yaml_tag = "!MultiplyByDefinition"

    def __init__(  # pylint: disable=R0913
        self, id1: str, text: str, definition_id: str
    ):
        super().__init__(id1, text, [])
        self.definition_id = definition_id

    def create_entries(self, design: Entry, parent: Entry) -> list[Entry]:
        ret: list[Entry] = []
        definition = op.find_entry_by_type_and_id(
            design, Definition, self.definition_id
        )

        for child_definition in definition.children:
            ret.append(copy.deepcopy(parent))
            last = ret[-1]
            last.id += "-" + (child_definition.get_id() or "NONE")
            if last.get_text():
                last.text += f" ({child_definition.get_id()})"
            last.children = copy.deepcopy(self.get_children())

        return ret
