from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Literal, NotRequired, Optional, TypedDict


@dataclass
class GCCDiagnostic:
    """
    See: https://gcc.gnu.org/onlinedocs/gcc-11.1.0/gcc/Diagnostic-Message-Formatting-Options.html
    """

    kind: Literal["error", "warning", "note"]
    # "If [kind] is warning, then there is an option key describing the command-line
    # option controlling the warning."
    option: Optional[str]
    # "A diagnostic can contain zero or more locations."
    locations: list[Location]
    message: str
    children: list[GCCDiagnostic]
    column_origin: Optional[int]
    escape_source: bool

    @staticmethod
    def from_item(parsed_item):
        return GCCDiagnostic(
            kind=parsed_item["kind"],
            message=parsed_item["message"],
            column_origin=parsed_item.get("column-origin"),
            locations=parse_locations(parsed_item["locations"]),
            children=GCCDiagnostic.from_list(parsed_item.get("children", ())),
            escape_source=parsed_item["escape-source"],
            option=parsed_item.get("option"),
        )

    @staticmethod
    def from_list(parsed_items):
        return [GCCDiagnostic.from_item(item) for item in parsed_items]

    @staticmethod
    def from_json_string(json_str: str | bytes) -> list[GCCDiagnostic]:
        return GCCDiagnostic.from_list(json.loads(json_str))


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
