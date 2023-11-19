from __future__ import annotations

import ctypes
import json
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Literal, NotRequired, Optional, TypedDict


@dataclass
class GCCDiagnostic:
    """
    See: https://gcc.gnu.org/onlinedocs/gcc-11.1.0/gcc/Diagnostic-Message-Formatting-Options.html
    """

    kind: Literal["error", "warning"]
    # "If [kind] is warning, then there is an option key describing the command-line
    # option controlling the warning."
    option: Optional[str]
    # "A diagnostic can contain zero or more locations."
    locations: list[Location]
    message: str
    children: list[GCCDiagnostic]
    column_origin: int
    escape_source: bool

    @staticmethod
    def from_item(parsed_item):
        return GCCDiagnostic(
            kind=parsed_item["kind"],
            message=parsed_item["message"],
            column_origin=parsed_item["column-origin"],
            locations=parse_locations(parsed_item["locations"]),
            children=GCCDiagnostic.from_list(parsed_item["children"]),
            escape_source=parsed_item["escape-source"],
            option=parsed_item.get("option"),
        )

    @staticmethod
    def from_list(parsed_items):
        return [GCCDiagnostic.from_item(item) for item in parsed_items]


class Location(TypedDict):
    """
    "Each location has an optional label string and up to three positions within it: a
    caret position and optional start and finish positions."
    """

    label: NotRequired[str]

    caret: Position
    start: NotRequired[Position]
    finish: NotRequired[Position]


def parse_locations(parsed_locations) -> list[Location]:
    return [parse_location(item) for item in parsed_locations]


def parse_location(item) -> Location:
    location: Location = {"caret": Position.from_item(item["caret"])}

    if label := item.get("label"):
        location["label"] = label

    if pos := item.get("start"):
        location["start"] = Position.from_item(pos)

    if pos := item.get("finish"):
        location["finish"] = Position.from_item(pos)

    return location


@dataclass
class Position:
    """
    "A position is described by a file name, a line number, and three numbers indicating
    a column position"
    """

    file: str
    line: int
    # "display-column counts display columns, accounting for tabs and multibyte
    # characters."
    display_column: int
    # "byte-column counts raw bytes."
    byte_column: int
    # "column is equal to one of the previous two, as dictated by the
    # -fdiagnostics-column-unit option."
    column: int

    @staticmethod
    def from_item(item) -> Position:
        return Position(
            file=item["file"],
            line=item["line"],
            display_column=item["display-column"],
            byte_column=item["byte-column"],
            column=item["column"],
        )


def print_as_python(diagnostic: GCCDiagnostic):
    # need absolute path to file
    # line number
    caret = diagnostic.locations[0]["caret"]
    full_path = Path(caret.file).resolve()
    line_num = caret.line
    # TODO: we're going to assume that the encoding of the file matches the encoding of
    # the output.
    column = caret.display_column
    initial_space = " " * (caret.display_column - 1)

    with full_path.open() as f:
        line = f.readlines()[line_num - 1].rstrip()

    # TODO: how is Python creating this message, and I how can I hack myself into that?
    # check traceback.py
    print(f'  File "{full_path}", line {line_num}')
    print(f"    {line}")
    print(f"    {initial_space}^")
    print(f"SyntaxError: {diagnostic.message}")


src = "hello.c"
# TODO: save the object file to some tmp dir?
# TODO: save the shared object to __pycache__?
status = subprocess.run(
    ["gcc-13", "-fdiagnostics-format=json", "-fPIC", "-c", src], capture_output=True
)
pems = GCCDiagnostic.from_list(json.loads(status.stderr))
if pems:
    assert status.returncode != 0
    print_as_python(pems[0])
    # TODO: this should raise a SyntaxError/ImportError, whichever is more relevant
assert status.returncode == 0

# Now link
# TODO: use distutils.ccompiler?
status = subprocess.run(
    ["gcc-13", "-shared", "-o", "libhello.dylib", "hello.o"], capture_output=True
)
if status.returncode != 0:
    raise NotImplementedError("linking failed and I don't know what to do")

libhello = ctypes.cdll.LoadLibrary("./libhello.dylib")
libhello.hello()
