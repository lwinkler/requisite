"""Generation of report in Markdown format"""

import io
import sys
import re
from xml.etree import ElementTree as ET
from pathlib import Path
from typing import Type
import entries as en

LINK_EXPRESSION = re.compile("<([a-zA-Z_][a-zA-Z0-9_-]*)>")


def get_id(entry: en.Entry) -> str:
    """Return the text if available"""
    if hasattr(entry, "id"):
        return entry.id
    return ""


def get_text(entry: en.Entry) -> str:
    """Return the text if available"""
    if hasattr(entry, "text"):
        return entry.text
    return ""

def wrap_id(entry: en.Entry) -> str:
    """Return the text if available"""
    a = ET.Element('a', attrib={'id': entry.id})
    a.text = get_id(entry)
    return a


def wrap_text(entry: en.Entry) -> str:
    """Return the text if available"""
    if not hasattr(entry, "text"):
        return ET.Element('p')
    html = re.sub(LINK_EXPRESSION, "<a href=\"#\\1\">\\1</a>", entry.text)
    return ET.fromstring('<p>' + html + '</p>')


def text_to_markdown(text: str) -> str:
    """Conversion to markdown text format"""
    results = re.sub(LINK_EXPRESSION, "[\\1](#\\1)", text)
    return html.escape(results)


def write_as_title_md(fout: io.TextIOWrapper, entry: en.Entry, level: int):
    fout.write("#" * level + " " + get_id(entry) + "\n")
    fout.write(text_to_markdown(get_text(entry)) + "\n")
    fout.write("\n")
    if hasattr(entry, "children"):
        for child in entry.children:
            write_as_title(fout, child, level + 1)

def class_to_p(cl: Type) -> str:
    """Write a class into a string"""
    p = ET.Element('b') #TODO rename
    p.text = cl.__name__.lower()[0:3]
    return p


def entry_to_p(entry: en.Entry) -> str:
    """Transform an entry into a string: for list"""
    #p = ET.Element('p')
    #p.append(class_to_p(type(entry)))
    #p.append(wrap_id(entry))
    id_str = f'<a id="{entry.id}">{entry.id}</a>' if hasattr(entry, "id") else ""
    cl_str = type(entry).__name__.lower()[0:3]
    text = re.sub(LINK_EXPRESSION, "<a href=\"#\\1\">\\1</a>", entry.text) if hasattr(entry, "text") else ""
    return ET.fromstring('<p>' + cl_str + id_str + text + '</p>')

def generate_list(entry: en.Entry, level: int) -> str:
    if not hasattr(entry, "children"):
        return entry_to_p(entry)

    p = entry_to_p(entry)
    ul = ET.Element('ul')
    p.append(ul)
    for child in entry.children:
        li = ET.Element('li')
        li.append(generate_list(child, level + 1))
        ul.append(li)
    return p


def write_report(output_path: Path, design: en.Entry) -> None:

    if output_path.is_file():
        print(f"File {output_path.as_posix()} already exists")
        sys.exit(1)
    with open(output_path, "w") as fout:

        # write_as_title_md(fout, design, 1)
        html = ET.Element('html')
        body = ET.Element('body')
        html.append(body)
        title = ET.Element('h1')
        title.text="Specs report " + get_id(design)
        body.append(title)
        body.append(generate_list(design, 1))

        tree = ET.ElementTree(html)
        ET.indent(tree, '  ')
        tree.write(fout, encoding='unicode',                                        method='html')

