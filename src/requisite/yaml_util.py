"""Utilities for YAML file format"""

import io
from pathlib import Path, WindowsPath
from ruamel.yaml import YAML, yaml_object
from typing import cast, Any, Callable, TypeVar

import entries as en

yaml = YAML(typ="safe")
yaml.sort_base_mapping_type_on_output = False
yaml.width = 100
# yaml.default_style = "|"

T = TypeVar("T")

# register external types
# path
def constr_path(constructor: Any, node: Any) -> Path:
    return Path(node.value)


def repr_path(representer: Any, data: Any) -> Any:
    return representer.represent_scalar("!Path", data.name)


yaml.representer.add_representer(WindowsPath, repr_path)
yaml.constructor.add_constructor("!Path", constr_path)

yaml.register_class(en.Entry)
yaml.register_class(en.Section)
yaml.register_class(en.Statement)
yaml.register_class(en.Definition)
yaml.register_class(en.Requirement)
yaml.register_class(en.Specification)
yaml.register_class(en.Test)
yaml.register_class(en.TestList)
yaml.register_class(en.Design)


def read_object(_: type[T], path: Path) -> T:
    """Read a full design document in YAML format"""
    with open(path, encoding="utf-8") as fin:
        obj = yaml.load(fin.read())
        # note: always keep the path for later
        obj.file_path = path
        return cast(T, obj)


def read_object_from_string(_: type[T], str1: str) -> T:
    """Read a full design document in YAML format"""
    return cast(T, yaml.load(str1))


def load_object(_: type[T], str_value: str) -> T:
    """Read a full design document in YAML format"""
    return cast(T, yaml.load(str_value))


def read_objects(_: type[T], path: Path) -> list[T]:
    """Read a list of entries in YAML format"""
    with open(path, encoding="utf-8") as fin:
        return cast(list[T], yaml.load(fin.read()))


def dump_entry(entry: en.Entry) -> bytes:
    """Dump and entry to a string"""
    # so far we set a very high line width
    buffer = io.BytesIO()
    yaml.dump(entry, buffer)
    return buffer.getvalue()
    return cast(str, yaml.dump(entry))  # , default_style="|")) # TODO


def write_entry(path: Path, design: en.Entry) -> None:
    """Write a full full design or entry in YAML format"""

    design.simplify()
    yaml.dump(design, path)
    return  # TODO

    with open(path, "w", encoding="utf-8") as fout:
        yaml.dump(design, fout)
        # fout.write(dump_entry(design))
