"""Generation of report in Markdown format"""

import io
import sys
import re
import html
from xml.etree import ElementTree as ET
from pathlib import Path
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


def wrap_id(entry: en.Entry) -> ET.Element:
    """Return the text if available"""
    a = ET.Element("a", attrib={"id": entry.id})
    a.text = get_id(entry)
    return a


def wrap_text(entry: en.Entry) -> ET.Element:
    """Return the text if available"""
    if not hasattr(entry, "text"):
        return ET.Element("p")
    html = re.sub(LINK_EXPRESSION, '<a href="#\\1">\\1</a>', entry.text)
    return ET.fromstring("<p>" + html + "</p>")


# TODO: Remove
def text_to_markdown(text: str) -> str:
    """Conversion to markdown text format"""
    results = re.sub(LINK_EXPRESSION, "[\\1](#\\1)", text)
    return html.escape(results)


def class_to_tag(entry: en.Entry) -> ET.Element:
    """Write a class into a string"""
    tag = ET.Element("b")
    if type(entry) == en.Specification:
        tag.text = "spec"
    else:
        tag.text = type(entry).__name__.lower()[0:3]
    return tag


def id_to_tag(entry: en.Entry, add_id: bool) -> ET.Element:
    """Write a class into a string"""
    id1 = get_id(entry)
    tag = ET.Element("a", attrib={"id": id1}) if add_id else ET.Element("a")
    tag.text = id1
    return tag


def entry_to_tag(entry: en.Entry, add_id: bool) -> ET.Element:
    """Transform an entry into a string: for list"""
    tag = ET.Element("p")
    tag.append(class_to_tag(entry))
    tag.append(id_to_tag(entry, add_id))
    text = (
        re.sub(LINK_EXPRESSION, '<a href="#\\1">\\1</a>', entry.text)
        if hasattr(entry, "text")
        else ""
    )
    tag.append(ET.fromstring("<a>" + text + "</a>"))
    return tag


def generate_list(entry: en.Entry, level: int) -> ET.Element:
    if not hasattr(entry, "children"):
        return entry_to_tag(entry, True)

    p = entry_to_tag(entry, True)
    ul = ET.Element("ul")
    p.append(ul)
    for child in entry.children:
        li = ET.Element("li")
        li.append(generate_list(child, level + 1))
        ul.append(li)
    return p


def write_report(output_path: Path, design: en.Entry) -> None:

    if output_path.is_file():
        print(f"File {output_path.as_posix()} already exists")
        sys.exit(1)
    with open(output_path, "w") as fout:

        # write_as_title_md(fout, design, 1)
        html = ET.Element("html")
        body = ET.Element("body")
        html.append(body)
        title = ET.Element("h1")
        title.text = "Specs report " + get_id(design)
        body.append(title)
        body.append(generate_list(design, 1))

        tree = ET.ElementTree(html)
        ET.indent(tree, "  ")
        tree.write(fout, encoding="unicode", method="html")
