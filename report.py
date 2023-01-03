"""Generation of specification report in HTML format"""

import re
from xml.etree import ElementTree as ET
from pathlib import Path
import entries as en
import operations as op
import verification as ve

LINK_EXPRESSION = re.compile("<([a-zA-Z_][a-zA-Z0-9_-]*)>")


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


def entry_to_div_tag(entry: en.Entry, add_id: bool) -> list[ET.Element]:
    """Transform an entry into a string: for list"""
    results: list[ET.Element] = []
    results.append(class_to_tag(entry))
    results.append(id_to_a_tag(entry, add_id))
    text = (
        re.sub(LINK_EXPRESSION, '<a href="#\\1">\\1</a>', entry.text)
        if hasattr(entry, "text")
        else ""
    )
    results.append(ET.fromstring("<a>" + text + "</a>"))
    return results


def generate_table_header() -> ET.Element:
    """Generate a tr header tag for the table"""
    tr_tag = ET.Element("tr")
    for title in ["type", "id", "verification", "text"]:
        th_tag = ET.SubElement(tr_tag, "th")
        th_tag.text = title
    return tr_tag


def get_verification_tag(entry: en.Statement, verifier: ve.Verifier) -> ET.Element:
    """Return a tag from the verification info of a statement"""

    ul_tag = ET.Element("ul")

    for verification_type in verifier.verify(entry):
        li_tag = ET.SubElement(ul_tag, "li")
        li_tag.text = verification_type.value
    return ul_tag


def entry_to_td(
    entry: en.Statement, verifier: ve.Verifier
) -> ET.Element:  # TODO: rename
    """Convert an id to a td tag"""
    tr_tag = ET.Element("tr")

    td_tag = ET.SubElement(tr_tag, "td")
    td_tag.append(class_to_tag(entry))

    td_tag = ET.SubElement(tr_tag, "td")
    td_tag.append(id_to_a_tag(entry, False))

    td_tag = ET.SubElement(tr_tag, "td")
    td_tag.append(get_verification_tag(entry, verifier))

    td_tag = ET.SubElement(tr_tag, "td")
    td_tag.append(wrap_text(entry))

    return tr_tag


def entry_to_table_tag(parent_entry: en.Entry, verifier: ve.Verifier) -> ET.Element:
    """Convert an entry to a table tag"""
    p_tag = ET.Element("p")
    for tag in entry_to_div_tag(parent_entry, True):
        p_tag.append(tag)
    table_tag = ET.SubElement(p_tag, "table")
    table_tag.append(generate_table_header())

    for statement in op.extract_entries_of_type(parent_entry, en.Statement):
        table_tag.append(entry_to_td(statement, verifier))

    return p_tag


def write_html_report(
    output_path: Path, design: en.Design, verifier: ve.Verifier
) -> None:
    """Write a HTML report to file"""

    # if output_path.is_file():
    # print(f"File {output_path.as_posix()} already exists")
    # sys.exit(1)
    with open(output_path, "w", encoding="utf-8") as fout:

        html_tag = ET.Element("html")
        head_tag = ET.SubElement(html_tag, "head")

        title_tag = ET.SubElement(head_tag, "title")
        title_tag.text = "Specifications " + design.get_id()

        head_tag.append(generate_style_tag())

        body_tag = ET.SubElement(html_tag, "body")

        h1_tag = ET.SubElement(body_tag, "h1")
        h1_tag.text = "Specifications " + design.get_id()

        # entry list
        h2_tag = ET.SubElement(body_tag, "h2")
        h2_tag.text = "Design tree"
        body_tag.append(entry_to_details_tag(design, True))

        h2_tag2 = ET.SubElement(body_tag, "h2")
        h2_tag2.text = "Statement table"
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
