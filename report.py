"""Generation of report in Markdown format"""

import sys
import html
import re
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

def text_to_markdown(text: str) -> str:
    """Conversion to markdown text format"""
    results = re.sub(LINK_EXPRESSION, "[\\1](#\\1)", text)
    return html.escape(results)

def write_as_title(fout: str, entry: en.Entry, level: int):
    fout.write("#" * level + " " + get_id(entry) + "\n")
    fout.write(text_to_markdown(get_text(entry)) + "\n")
    fout.write("\n")
    if hasattr(entry, "children"):
        for child in entry.children:
            write_as_title(fout, child, level + 1)

def write_report(output_path: Path, design: en.Entry) -> None:

    if output_path.is_file():
        print(f"File {output_path.as_posix()} already exists")
        sys.exit(1)
    with open(output_path, "w") as fout:

        write_as_title(fout, design, 1)
