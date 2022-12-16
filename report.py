"""Generation of specification report in HTML format"""

import re
from xml.etree import ElementTree as ET
from enum import Enum
from pathlib import Path
from typing import List, cast
import entries as en
import operations as op

LINK_EXPRESSION = re.compile("<([a-zA-Z_][a-zA-Z0-9_-]*)>")


class VerificationType(Enum):
    """How a statement can be verified"""

    TEST = "test"
    CHILDREN = "children"


# TODO: add method and test
class Verifier:
    """Object that contains the verification information of the design"""

    def __init__(self, design: en.Design):
        self.verified_ids = [
            test.verify_id
            for test in cast(List[en.Test], op.extract_entries_of_type(design, en.Test))
        ]

    def verify(self, statement: en.Statement) -> List[VerificationType]:
        """Verify a statement"""
        results: List[VerificationType] = []
        if statement.id in self.verified_ids:
            results.append(VerificationType.TEST)
        if statement.get_children():
            results.append(VerificationType.CHILDREN)
        return results


def wrap_text(entry: en.Entry) -> ET.Element:
    """Return the text if available"""
    if not hasattr(entry, "text"):
        return ET.Element("p")
    html_str = re.sub(LINK_EXPRESSION, '<a href="#\\1">\\1</a>', entry.text)
    return ET.fromstring("<p>" + html_str + "</p>")


def class_to_tag(entry: en.Entry) -> ET.Element:
    """Write a class into a string"""
    tag = ET.Element("b", attrib={"title": type(entry).__name__})
    tag.text = entry.short_type
    return tag


def id_to_a_tag(entry: en.Entry, add_id: bool) -> ET.Element:
    """Write a class into a string"""
    attributes = {"id": entry.get_id()} if add_id else {"href": "#" + entry.get_id()}
    tag = ET.Element("a", attrib=attributes)
    tag.text = entry.get_id()
    return tag


def entry_to_details_tag(entry: en.Entry, add_id: bool) -> ET.Element:
    """Transform an entry into a string: for list"""
    details_tag = ET.Element("details")
    summary_tag = ET.Element("summary")
    for tag in entry_to_div_tag(entry, add_id):
        summary_tag.append(tag)
    details_tag.append(summary_tag)
    for child in entry.get_children():
        if child.get_children():
            details_tag.append(entry_to_details_tag(child, add_id))
        else:
            p_tag = ET.Element("p")
            for tag in entry_to_div_tag(child, add_id):
                p_tag.append(tag)
            details_tag.append(p_tag)
    return details_tag

def entry_to_div_tag(entry: en.Entry, add_id: bool) -> List[ET.Element]:
    """Transform an entry into a string: for list"""
    results: List[ET.Element] = []
    results.append(class_to_tag(entry))
    results.append(id_to_a_tag(entry, add_id))
    text = (
        re.sub(LINK_EXPRESSION, '<a href="#\\1">\\1</a>', entry.text)
        if hasattr(entry, "text")
        else ""
    )
    results.append(ET.fromstring("<a>" + text + "</a>"))
    return results


def generate_list_tag(entry: en.Entry, level: int) -> ET.Element:
    """Generate a list tag from entry"""
    if not entry.get_children():
        return entry_to_div_tag(entry, True)

    p_tag = entry_to_div_tag(entry, True)
    ul_tag = ET.Element("ul")
    p_tag.append(ul_tag)
    for child in entry.children:
        li_tag = ET.Element("li")
        li_tag.append(generate_list_tag(child, level + 1))
        ul_tag.append(li_tag)
    return p_tag


def generate_table_header() -> ET.Element:
    """Generate a tr header tag for the table"""
    tr_tag = ET.Element("tr")
    for title in ["type", "id", "verification", "text"]:
        th_tag = ET.Element("th")
        th_tag.text = title
        tr_tag.append(th_tag)
    return tr_tag


def get_verification_tag(entry: en.Entry, verifier: Verifier) -> ET.Element:
    """Return a tag from the verification info of a statement"""

    ul_tag = ET.Element("ul")

    for verification_type in verifier.verify(cast(en.Statement, entry)):
        li_tag = ET.Element("li")
        li_tag.text = verification_type.value
        ul_tag.append(li_tag)
    return ul_tag


def entry_to_td(entry: en.Entry, verifier: Verifier) -> ET.Element:
    """Convert an id to a td tag"""
    tr_tag = ET.Element("tr")

    td_tag = ET.Element("td")
    td_tag.append(class_to_tag(entry))
    tr_tag.append(td_tag)

    td_tag = ET.Element("td")
    td_tag.append(id_to_a_tag(entry, False))
    tr_tag.append(td_tag)

    td_tag = ET.Element("td")
    td_tag.append(get_verification_tag(entry, verifier))
    tr_tag.append(td_tag)

    td_tag = ET.Element("td")
    td_tag.append(wrap_text(entry))
    tr_tag.append(td_tag)

    return tr_tag


def entry_to_table_tag(parent_entry: en.Entry, verifier: Verifier) -> ET.Element:
    """Convert an entry to a table tag"""
    p_tag = ET.Element("p")
    for tag in entry_to_div_tag(parent_entry, True):
        p_tag.append(tag)
    table_tag = ET.Element("table")
    p_tag.append(table_tag)
    table_tag.append(generate_table_header())

    for entry in op.extract_entries_of_type(parent_entry, en.Statement):
        table_tag.append(entry_to_td(entry, verifier))

    return p_tag


def write_html_report(output_path: Path, design: en.Design) -> None:
    """Write a HTML report to file"""

    verifier = Verifier(design)

    # if output_path.is_file():
    # print(f"File {output_path.as_posix()} already exists")
    # sys.exit(1)
    with open(output_path, "w", encoding="utf-8") as fout:

        html_tag = ET.Element("html")
        head_tag = ET.Element("head")
        html_tag.append(head_tag)

        title_tag = ET.Element("title")
        title_tag.text = "Specs report " + design.get_id()
        head_tag.append(title_tag)

        head_tag.append(generate_style_tag())

        body_tag = ET.Element("body")
        html_tag.append(body_tag)

        h1_tag = ET.Element("h1")
        h1_tag.text = "Specs report " + design.get_id()
        body_tag.append(h1_tag)

        # entry list
        # body_tag.append(generate_list_tag(design, 1))
        body_tag.append(entry_to_details_tag(design, True))

        body_tag.append(entry_to_table_tag(design, verifier))

        tree = ET.ElementTree(html_tag)
        ET.indent(tree, "  ")
        tree.write(fout, encoding="unicode", method="html")


def generate_style_tag() -> ET.Element:
    """Generate the style tag containing the CSS"""

    style_tag = ET.Element("style", attrib={"type": "text/css"})
    style_tag.text = """
table ul {
    list-style: none;
}

table {
    border: 1px solid black;
    width: 800px;
}

table th {
    border-bottom: 1px solid black;
    background-color: silver;
}

table td {
    border-bottom: 1px solid gray;
}

td.ok {
    border-bottom: 1px solid gray;
    background-color: green;
}

td.failure {
    border-bottom: 1px solid gray;
    background-color: red;
}

td.notperformed {
    border-bottom: 1px solid gray;
    background-color: white;
}

.test-result-describe-cell {
    background-color: tan;
    font-style: italic;
}

.test-cast-status-box-ok {
    border: 1px solid black;
    float: left;
    margin-right: 10px;
    width: 45px;
    height: 25px;
    background-color: green;
}

/* for details */
details {
    border: 1px solid #aaa;
    border-radius: 4px;
    padding: .5em .5em 0;
}

summary {
    font-weight: bold;
    margin: -.5em -.5em 0;
    padding: .5em;
}

details[open] {
    padding: .5em;
}

details[open] summary {
    border-bottom: 1px solid #aaa;
    margin-bottom: .5em;
}

"""
    return style_tag
