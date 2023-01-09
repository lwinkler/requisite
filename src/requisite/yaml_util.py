"""Utilities for YAML file format"""

import io
from pathlib import Path, WindowsPath
from ruamel.yaml import YAML, yaml_object
from typing import cast, TypeVar

import entries as en

yaml = YAML(typ="safe")

T = TypeVar("T")

# register types
# ruamel
def constr_path(constructor, node):
    return Path(node.value)
def repr_path(representer, data):
    return representer.represent_scalar(u'!Path', data.name)
yaml.representer.add_representer(WindowsPath, repr_path)
yaml.constructor.add_constructor(u'!Path', constr_path)

yaml.register_class(en.Entry)
yaml.register_class(en.Section)
yaml.register_class(en.Statement)
yaml.register_class(en.Definition)
yaml.register_class(en.Requirement)
yaml.register_class(en.Specification)
yaml.register_class(en.Test)
yaml.register_class(en.TestList)
yaml.register_class(en.Design)

# def path_constructor(loader,node):
    # value = loader.construct_scalar(node)
    # print(111, value, node)
    # # someNumber,sep,someString = value.partition("|")
    # return Path(value)
# 
# def path_representer(dumper, data):
    # return dumper.represent_scalar('!Path', data.as_posix() )
# 
# yaml.add_constructor('!Path', path_constructor)
# yaml.add_representer(WindowsPath, path_representer)


# path = Path("./my/path")
#TODO clean
# assert(path.as_posix() == "my/path")
# print(66, yaml.dump(path), yaml.dump(path) == "!Path 'my/path'\n")
# assert(yaml.dump(path) == "!Path 'my/path'\n")
# 
# path = yaml.unsafe_load(yaml.dump(path))
# assert(path.as_posix() == "my/path")
# 
# exit(88)

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
    return cast(
        str, yaml.dump(entry) # TODO , width=1000, sort_keys=False)
    )  # , default_style="|"))


def write_entry(path: Path, design: en.Entry) -> None:
    """Write a full full design or entry in YAML format"""

    design.simplify()
    yaml.dump(design, path)
    return # TODO

    with open(path, "w", encoding="utf-8") as fout:
        yaml.dump(design, fout)
        # fout.write(dump_entry(design))
