"""Generation of specification report in HTML format"""

import re
from xml.etree import ElementTree as ET
from pathlib import Path
import entries as en
import operations as op

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
    tag = ET.Element("a", attrib={"id": entry.id})
    tag.text = get_id(entry)
    return tag


def wrap_text(entry: en.Entry) -> ET.Element:
    """Return the text if available"""
    if not hasattr(entry, "text"):
        return ET.Element("p")
    html_str = re.sub(LINK_EXPRESSION, '<a href="#\\1">\\1</a>', entry.text)
    return ET.fromstring("<p>" + html_str + "</p>")


def class_to_tag(entry: en.Entry) -> ET.Element:
    """Write a class into a string"""
    tag = ET.Element("b")
    if type(entry) == en.Specification:  # pylint: disable=C0123
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


def generate_list_tag(entry: en.Entry, level: int) -> ET.Element:
    """Generate a list tag from entry"""
    if not entry.get_children():
        return entry_to_tag(entry, True)

    p_tag = entry_to_tag(entry, True)
    ul_tag = ET.Element("ul")
    p_tag.append(ul_tag)
    for child in entry.children:
        li_tag = ET.Element("li")
        li_tag.append(generate_list_tag(child, level + 1))
        ul_tag.append(li_tag)
    return p_tag

def generate_table_header() -> ET.Element:
    tr_tag = ET.Element("tr")
    for title in ["type", "id", "text"]:
        th_tag = ET.Element("th")
        th_tag.text = title
        tr_tag.append(th_tag)
    return tr_tag

def entry_to_td(entry: en.Entry) -> ET.Element:
    tr_tag = ET.Element("tr")

    td_tag = ET.Element("td")
    td_tag.text = type(entry).__name__
    tr_tag.append(td_tag)

    td_tag = ET.Element("td")
    td_tag.text = entry.get_id()
    tr_tag.append(td_tag)

    td_tag = ET.Element("td")
    td_tag.text = entry.get_text()
    tr_tag.append(td_tag)

    return tr_tag


def generate_table_tag(parent_entry: en.Entry) -> ET.Element:
    p_tag = entry_to_tag(parent_entry, True)
    table_tag = ET.Element("table")
    p_tag.append(table_tag)
    table_tag.append(generate_table_header())

    for entry in op.extract_entries_of_type(parent_entry, en.Statement):
        table_tag.append(entry_to_td(entry))

    return p_tag
     
def write_html_report(output_path: Path, design: en.Entry) -> None:
    """Write a HTML report to file"""

    # if output_path.is_file():
    # print(f"File {output_path.as_posix()} already exists")
    # sys.exit(1)
    with open(output_path, "w", encoding="utf-8") as fout:

        html_tag = ET.Element("html")
        body_tag = ET.Element("body")
        html_tag.append(body_tag)
        title_tag = ET.Element("h1")
        title_tag.text = "Specs report " + get_id(design)
        body_tag.append(title_tag)

        # entry list
        body_tag.append(generate_list_tag(design, 1))

        body_tag.append(generate_table_tag(design))

        tree = ET.ElementTree(html_tag)
        ET.indent(tree, "  ")
        tree.write(fout, encoding="unicode", method="html")
