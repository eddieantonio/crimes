import pytest

from language_bender.gcc_diagnostics import GCCDiagnostic, Position

TEST_CASES = [
    (
        b'[{"kind": "error", "message": "too few arguments to function \'quack\'", "'
        b'children": [], "column-origin": 1, "locations": [{"caret": {"file": "15-'
        b'e1017.c", "line": 3, "display-column": 5, "byte-column": 5, "column": 5}'
        b', "finish": {"file": "15-e1017.c", "line": 3, "display-column": 9, "byte'
        b'-column": 9, "column": 9}}], "escape-source": false}, {"kind": "note", "'
        b'message": "declared here", "children": [], "column-origin": 1, "location'
        b's": [{"caret": {"file": "15-e1017.c", "line": 1, "display-column": 6, "b'
        b'yte-column": 6, "column": 6}, "finish": {"file": "15-e1017.c", "line": 1'
        b', "display-column": 10, "byte-column": 10, "column": 10}}], "escape-sour'
        b'ce": false}]\n',
        [
            GCCDiagnostic(
                kind="error",
                option=None,
                locations=[
                    {
                        "caret": Position(
                            file="15-e1017.c",
                            line=3,
                            display_column=5,
                            byte_column=5,
                            column=5,
                        ),
                        "finish": Position(
                            file="15-e1017.c",
                            line=3,
                            display_column=9,
                            byte_column=9,
                            column=9,
                        ),
                    }
                ],
                message="too few arguments to function 'quack'",
                children=[],
                column_origin=1,
                escape_source=False,
            ),
            GCCDiagnostic(
                kind="note",
                option=None,
                locations=[
                    {
                        "caret": Position(
                            file="15-e1017.c",
                            line=1,
                            display_column=6,
                            byte_column=6,
                            column=6,
                        ),
                        "finish": Position(
                            file="15-e1017.c",
                            line=1,
                            display_column=10,
                            byte_column=10,
                            column=10,
                        ),
                    }
                ],
                message="declared here",
                children=[],
                column_origin=1,
                escape_source=False,
            ),
        ],
    ),
    (
        b'[{"kind": "error", "message": "stray \'`\' in program", "children": [], "c'
        b'olumn-origin": 1, "locations": [{"caret": {"file": "03-e1007.c", "line":'
        b' 1, "display-column": 24, "byte-column": 24, "column": 24}}], "escape-so'
        b'urce": false}]\n',
        [
            GCCDiagnostic(
                kind="error",
                option=None,
                locations=[
                    {
                        "caret": Position(
                            file="03-e1007.c",
                            line=1,
                            display_column=24,
                            byte_column=24,
                            column=24,
                        )
                    }
                ],
                message="stray '`' in program",
                children=[],
                column_origin=1,
                escape_source=False,
            )
        ],
    ),
    (
        b'[{"kind": "error", "message": "expected \';\' before \'int\'", "children'
        b'": [], "column-origin": 1, "locations": [{"caret": {"file": "02-e1002.c"'
        b', "line": 1, "display-column": 6, "byte-column": 6, "column": 6}}, {"car'
        b'et": {"file": "02-e1002.c", "line": 2, "display-column": 1, "byte-column'
        b'": 1, "column": 1}, "finish": {"file": "02-e1002.c", "line": 2, "display'
        b'-column": 3, "byte-column": 3, "column": 3}}], "fixits": [{"start": {"fi'
        b'le": "02-e1002.c", "line": 1, "display-column": 6, "byte-column": 6, "co'
        b'lumn": 6}, "next": {"file": "02-e1002.c", "line": 1, "display-column": 6'
        b', "byte-column": 6, "column": 6}, "string": ";"}], "escape-source": fals'
        b"e}]\n",
        [
            GCCDiagnostic(
                kind="error",
                option=None,
                locations=[
                    {
                        "caret": Position(
                            file="02-e1002.c",
                            line=1,
                            display_column=6,
                            byte_column=6,
                            column=6,
                        )
                    },
                    {
                        "caret": Position(
                            file="02-e1002.c",
                            line=2,
                            display_column=1,
                            byte_column=1,
                            column=1,
                        ),
                        "finish": Position(
                            file="02-e1002.c",
                            line=2,
                            display_column=3,
                            byte_column=3,
                            column=3,
                        ),
                    },
                ],
                message="expected ';' before 'int'",
                children=[],
                column_origin=1,
                escape_source=False,
            )
        ],
    ),
    (
        b'[{"kind": "error", "message": "\'Duck\' has no member named \'quack\'", '
        b'"children": [], "column-origin": 1, "locations": [{"caret": {"file": "11'
        b'-e1012.c", "line": 7, "display-column": 16, "byte-column": 16, "column":'
        b' 16}}], "escape-source": false}]\n',
        [
            GCCDiagnostic(
                kind="error",
                option=None,
                locations=[
                    {
                        "caret": Position(
                            file="11-e1012.c",
                            line=7,
                            display_column=16,
                            byte_column=16,
                            column=16,
                        )
                    }
                ],
                message="'Duck' has no member named 'quack'",
                children=[],
                column_origin=1,
                escape_source=False,
            )
        ],
    ),
    (
        b'[{"kind": "error", "message": "\'duck\' undeclared (first use in this func'
        b'tion)", "children": [{"kind": "note", "message": "each undeclared identi'
        b'fier is reported only once for each function it appears in", "locations"'
        b': [{"caret": {"file": "01-e1001.c", "line": 2, "display-column": 12, "by'
        b'te-column": 12, "column": 12}, "finish": {"file": "01-e1001.c", "line": '
        b'2, "display-column": 15, "byte-column": 15, "column": 15}}], "escape-sou'
        b'rce": false}], "column-origin": 1, "locations": [{"caret": {"file": "01-'
        b'e1001.c", "line": 2, "display-column": 12, "byte-column": 12, "column": '
        b'12}, "finish": {"file": "01-e1001.c", "line": 2, "display-column": 15, "'
        b'byte-column": 15, "column": 15}}], "escape-source": false}]\n',
        [
            GCCDiagnostic(
                kind="error",
                option=None,
                locations=[
                    {
                        "caret": Position(
                            file="01-e1001.c",
                            line=2,
                            display_column=12,
                            byte_column=12,
                            column=12,
                        ),
                        "finish": Position(
                            file="01-e1001.c",
                            line=2,
                            display_column=15,
                            byte_column=15,
                            column=15,
                        ),
                    }
                ],
                message="'duck' undeclared (first use in this function)",
                children=[
                    GCCDiagnostic(
                        kind="note",
                        option=None,
                        locations=[
                            {
                                "caret": Position(
                                    file="01-e1001.c",
                                    line=2,
                                    display_column=12,
                                    byte_column=12,
                                    column=12,
                                ),
                                "finish": Position(
                                    file="01-e1001.c",
                                    line=2,
                                    display_column=15,
                                    byte_column=15,
                                    column=15,
                                ),
                            }
                        ],
                        message="each undeclared identifier "
                        "is reported only once for "
                        "each function it appears in",
                        children=[],
                        column_origin=None,
                        escape_source=False,
                    )
                ],
                column_origin=1,
                escape_source=False,
            )
        ],
    ),
    (
        b'[{"kind": "error", "message": "invalid type argument of \'->\' (have \''
        b'int\')", "children": [], "column-origin": 1, "locations": [{"caret": {"fi'
        b'le": "13-e1013.c", "line": 2, "display-column": 16, "byte-column": 16, "'
        b'column": 16}, "finish": {"file": "13-e1013.c", "line": 2, "display-colum'
        b'n": 17, "byte-column": 17, "column": 17}}], "escape-source": false}]\n',
        [
            GCCDiagnostic(
                kind="error",
                option=None,
                locations=[
                    {
                        "caret": Position(
                            file="13-e1013.c",
                            line=2,
                            display_column=16,
                            byte_column=16,
                            column=16,
                        ),
                        "finish": Position(
                            file="13-e1013.c",
                            line=2,
                            display_column=17,
                            byte_column=17,
                            column=17,
                        ),
                    }
                ],
                message="invalid type argument of '->' (have 'int')",
                children=[],
                column_origin=1,
                escape_source=False,
            )
        ],
    ),
    (
        b'[{"kind": "warning", "message": "missing terminating \\" character", "chi'
        b'ldren": [{"kind": "error", "message": "missing terminating \\" character"'
        b', "locations": [{"caret": {"file": "19-e1015.c", "line": 1, "display-col'
        b'umn": 17, "byte-column": 17, "column": 17}}], "escape-source": false}], '
        b'"column-origin": 1, "locations": [{"caret": {"file": "19-e1015.c", "line'
        b'": 1, "display-column": 17, "byte-column": 17, "column": 17}}], "escape-'
        b'source": false}, {"kind": "error", "message": "expected expression befor'
        b'e \';\' token", "children": [], "column-origin": 1, "locations": [{"caret"'
        b': {"file": "19-e1015.c", "line": 2, "display-column": 1, "byte-column": '
        b'1, "column": 1}}], "escape-source": false}]\n',
        [
            GCCDiagnostic(
                kind="warning",
                option=None,
                locations=[
                    {
                        "caret": Position(
                            file="19-e1015.c",
                            line=1,
                            display_column=17,
                            byte_column=17,
                            column=17,
                        )
                    }
                ],
                message='missing terminating " character',
                children=[
                    GCCDiagnostic(
                        kind="error",
                        option=None,
                        locations=[
                            {
                                "caret": Position(
                                    file="19-e1015.c",
                                    line=1,
                                    display_column=17,
                                    byte_column=17,
                                    column=17,
                                )
                            }
                        ],
                        message='missing terminating " ' "character",
                        children=[],
                        column_origin=None,
                        escape_source=False,
                    )
                ],
                column_origin=1,
                escape_source=False,
            ),
            GCCDiagnostic(
                kind="error",
                option=None,
                locations=[
                    {
                        "caret": Position(
                            file="19-e1015.c",
                            line=2,
                            display_column=1,
                            byte_column=1,
                            column=1,
                        )
                    }
                ],
                message="expected expression before ';' token",
                children=[],
                column_origin=1,
                escape_source=False,
            ),
        ],
    ),
    (
        b'[{"kind": "error", "message": "redefinition of \'number_of_quacks\'", "chi'
        b'ldren": [{"kind": "note", "message": "previous definition of \'number_of_'
        b'quacks\' with type \'int\'", "locations": [{"caret": {"file": "20-e1020.c",'
        b' "line": 1, "display-column": 5, "byte-column": 5, "column": 5}, "finish'
        b'": {"file": "20-e1020.c", "line": 1, "display-column": 20, "byte-column"'
        b': 20, "column": 20}}], "escape-source": false}], "column-origin": 1, "lo'
        b'cations": [{"caret": {"file": "20-e1020.c", "line": 2, "display-column":'
        b' 5, "byte-column": 5, "column": 5}, "finish": {"file": "20-e1020.c", "li'
        b'ne": 2, "display-column": 20, "byte-column": 20, "column": 20}}], "escap'
        b'e-source": false}]\n',
        [
            GCCDiagnostic(
                kind="error",
                option=None,
                locations=[
                    {
                        "caret": Position(
                            file="20-e1020.c",
                            line=2,
                            display_column=5,
                            byte_column=5,
                            column=5,
                        ),
                        "finish": Position(
                            file="20-e1020.c",
                            line=2,
                            display_column=20,
                            byte_column=20,
                            column=20,
                        ),
                    }
                ],
                message="redefinition of 'number_of_quacks'",
                children=[
                    GCCDiagnostic(
                        kind="note",
                        option=None,
                        locations=[
                            {
                                "caret": Position(
                                    file="20-e1020.c",
                                    line=1,
                                    display_column=5,
                                    byte_column=5,
                                    column=5,
                                ),
                                "finish": Position(
                                    file="20-e1020.c",
                                    line=1,
                                    display_column=20,
                                    byte_column=20,
                                    column=20,
                                ),
                            }
                        ],
                        message="previous definition of "
                        "'number_of_quacks' with type "
                        "'int'",
                        children=[],
                        column_origin=None,
                        escape_source=False,
                    )
                ],
                column_origin=1,
                escape_source=False,
            )
        ],
    ),
    (
        b'[{"kind": "error", "message": "expected identifier or \'(\' before \'{\''
        b' token", "children": [], "column-origin": 1, "locations": [{"caret": {"f'
        b'ile": "alt-07-e1008.c", "line": 1, "display-column": 9, "byte-column": 9'
        b', "column": 9}}], "escape-source": false}]\n',
        [
            GCCDiagnostic(
                kind="error",
                option=None,
                locations=[
                    {
                        "caret": Position(
                            file="alt-07-e1008.c",
                            line=1,
                            display_column=9,
                            byte_column=9,
                            column=9,
                        )
                    }
                ],
                message="expected identifier or '(' before '{' token",
                children=[],
                column_origin=1,
                escape_source=False,
            )
        ],
    ),
    (
        b'[{"kind": "error", "message": "expected identifier or \'(\' before \'ch'
        b'ar\'", "children": [], "column-origin": 1, "locations": [{"caret": {"file'
        b'": "07-e1006.c", "line": 1, "display-column": 11, "byte-column": 11, "co'
        b'lumn": 11}, "finish": {"file": "07-e1006.c", "line": 1, "display-column"'
        b': 14, "byte-column": 14, "column": 14}}], "escape-source": false}]\n',
        [
            GCCDiagnostic(
                kind="error",
                option=None,
                locations=[
                    {
                        "caret": Position(
                            file="07-e1006.c",
                            line=1,
                            display_column=11,
                            byte_column=11,
                            column=11,
                        ),
                        "finish": Position(
                            file="07-e1006.c",
                            line=1,
                            display_column=14,
                            byte_column=14,
                            column=14,
                        ),
                    }
                ],
                message="expected identifier or '(' before 'char'",
                children=[],
                column_origin=1,
                escape_source=False,
            )
        ],
    ),
    (
        b'[{"kind": "error", "message": "lvalue required as increment operand", "c'
        b'hildren": [], "column-origin": 1, "locations": [{"caret": {"file": "16-e'
        b'1011.c", "line": 2, "display-column": 5, "byte-column": 5, "column": 5},'
        b' "finish": {"file": "16-e1011.c", "line": 2, "display-column": 6, "byte-'
        b'column": 6, "column": 6}}], "escape-source": false}]\n',
        [
            GCCDiagnostic(
                kind="error",
                option=None,
                locations=[
                    {
                        "caret": Position(
                            file="16-e1011.c",
                            line=2,
                            display_column=5,
                            byte_column=5,
                            column=5,
                        ),
                        "finish": Position(
                            file="16-e1011.c",
                            line=2,
                            display_column=6,
                            byte_column=6,
                            column=6,
                        ),
                    }
                ],
                message="lvalue required as increment operand",
                children=[],
                column_origin=1,
                escape_source=False,
            )
        ],
    ),
    (
        b'[{"kind": "error", "message": "expected expression before \'int\'", "child'
        b'ren": [], "column-origin": 1, "locations": [{"caret": {"file": "04-e1004'
        b'.c", "line": 2, "display-column": 12, "byte-column": 12, "column": 12}, '
        b'"finish": {"file": "04-e1004.c", "line": 2, "display-column": 14, "byte-'
        b'column": 14, "column": 14}}], "escape-source": false}]\n',
        [
            GCCDiagnostic(
                kind="error",
                option=None,
                locations=[
                    {
                        "caret": Position(
                            file="04-e1004.c",
                            line=2,
                            display_column=12,
                            byte_column=12,
                            column=12,
                        ),
                        "finish": Position(
                            file="04-e1004.c",
                            line=2,
                            display_column=14,
                            byte_column=14,
                            column=14,
                        ),
                    }
                ],
                message="expected expression before 'int'",
                children=[],
                column_origin=1,
                escape_source=False,
            )
        ],
    ),
    (
        b'[{"kind": "error", "message": "expected declaration specifiers or \'...\' '
        b'before string constant", "children": [], "column-origin": 1, "locations"'
        b': [{"caret": {"file": "10-e1044.c", "line": 1, "display-column": 8, "byt'
        b'e-column": 8, "column": 8}, "finish": {"file": "10-e1044.c", "line": 1, '
        b'"display-column": 23, "byte-column": 23, "column": 23}}], "escape-source'
        b'": false}]\n',
        [
            GCCDiagnostic(
                kind="error",
                option=None,
                locations=[
                    {
                        "caret": Position(
                            file="10-e1044.c",
                            line=1,
                            display_column=8,
                            byte_column=8,
                            column=8,
                        ),
                        "finish": Position(
                            file="10-e1044.c",
                            line=1,
                            display_column=23,
                            byte_column=23,
                            column=23,
                        ),
                    }
                ],
                message="expected declaration specifiers or '...' before "
                "string constant",
                children=[],
                column_origin=1,
                escape_source=False,
            )
        ],
    ),
    (
        b'[{"kind": "error", "message": "expected declaration specifiers or \'...\' '
        b'before numeric constant", "children": [], "column-origin": 1, "locations'
        b'": [{"caret": {"file": "17-e1022.c", "line": 1, "display-column": 10, "b'
        b'yte-column": 10, "column": 10}, "finish": {"file": "17-e1022.c", "line":'
        b' 1, "display-column": 11, "byte-column": 11, "column": 11}}], "escape-so'
        b'urce": false}]\n',
        [
            GCCDiagnostic(
                kind="error",
                option=None,
                locations=[
                    {
                        "caret": Position(
                            file="17-e1022.c",
                            line=1,
                            display_column=10,
                            byte_column=10,
                            column=10,
                        ),
                        "finish": Position(
                            file="17-e1022.c",
                            line=1,
                            display_column=11,
                            byte_column=11,
                            column=11,
                        ),
                    }
                ],
                message="expected declaration specifiers or '...' before "
                "numeric constant",
                children=[],
                column_origin=1,
                escape_source=False,
            )
        ],
    ),
    (
        b'[{"kind": "error", "message": "request for member \'length\' in something '
        b'not a structure or union", "children": [], "column-origin": 1, "location'
        b's": [{"caret": {"file": "09-e1023.c", "line": 2, "display-column": 16, "'
        b'byte-column": 16, "column": 16}}], "escape-source": false}]\n',
        [
            GCCDiagnostic(
                kind="error",
                option=None,
                locations=[
                    {
                        "caret": Position(
                            file="09-e1023.c",
                            line=2,
                            display_column=16,
                            byte_column=16,
                            column=16,
                        )
                    }
                ],
                message="request for member 'length' in something not a "
                "structure or union",
                children=[],
                column_origin=1,
                escape_source=False,
            )
        ],
    ),
    (
        b'[{"kind": "error", "message": "unknown type name \'integer\'", "children":'
        b' [], "column-origin": 1, "locations": [{"caret": {"file": "05-e1010.c", '
        b'"line": 1, "display-column": 1, "byte-column": 1, "column": 1}, "finish"'
        b': {"file": "05-e1010.c", "line": 1, "display-column": 7, "byte-column": '
        b'7, "column": 7}}], "escape-source": false}]\n',
        [
            GCCDiagnostic(
                kind="error",
                option=None,
                locations=[
                    {
                        "caret": Position(
                            file="05-e1010.c",
                            line=1,
                            display_column=1,
                            byte_column=1,
                            column=1,
                        ),
                        "finish": Position(
                            file="05-e1010.c",
                            line=1,
                            display_column=7,
                            byte_column=7,
                            column=7,
                        ),
                    }
                ],
                message="unknown type name 'integer'",
                children=[],
                column_origin=1,
                escape_source=False,
            )
        ],
    ),
    (
        b'[{"kind": "error", "message": "expected \')\' before numeric constant", "c'
        b'hildren": [], "column-origin": 1, "locations": [{"caret": {"file": "14-e'
        b'1030.c", "line": 3, "display-column": 19, "byte-column": 19, "column": 1'
        b'9}}, {"caret": {"file": "14-e1030.c", "line": 3, "display-column": 20, "'
        b'byte-column": 20, "column": 20}, "finish": {"file": "14-e1030.c", "line"'
        b': 3, "display-column": 21, "byte-column": 21, "column": 21}}, {"caret": '
        b'{"file": "14-e1030.c", "line": 3, "display-column": 11, "byte-column": 1'
        b'1, "column": 11}}], "fixits": [{"start": {"file": "14-e1030.c", "line": '
        b'3, "display-column": 19, "byte-column": 19, "column": 19}, "next": {"fil'
        b'e": "14-e1030.c", "line": 3, "display-column": 19, "byte-column": 19, "c'
        b'olumn": 19}, "string": ")"}], "escape-source": false}]\n',
        [
            GCCDiagnostic(
                kind="error",
                option=None,
                locations=[
                    {
                        "caret": Position(
                            file="14-e1030.c",
                            line=3,
                            display_column=19,
                            byte_column=19,
                            column=19,
                        )
                    },
                    {
                        "caret": Position(
                            file="14-e1030.c",
                            line=3,
                            display_column=20,
                            byte_column=20,
                            column=20,
                        ),
                        "finish": Position(
                            file="14-e1030.c",
                            line=3,
                            display_column=21,
                            byte_column=21,
                            column=21,
                        ),
                    },
                    {
                        "caret": Position(
                            file="14-e1030.c",
                            line=3,
                            display_column=11,
                            byte_column=11,
                            column=11,
                        )
                    },
                ],
                message="expected ')' before numeric constant",
                children=[],
                column_origin=1,
                escape_source=False,
            )
        ],
    ),
    (
        b'[{"kind": "error", "message": "expected declaration or statement at end '
        b'of input", "children": [], "column-origin": 1, "locations": [{"caret": {'
        b'"file": "06-e1005.c", "line": 1, "display-column": 1, "byte-column": 1, '
        b'"column": 1}, "finish": {"file": "06-e1005.c", "line": 1, "display-colum'
        b'n": 3, "byte-column": 3, "column": 3}}], "escape-source": false}]\n',
        [
            GCCDiagnostic(
                kind="error",
                option=None,
                locations=[
                    {
                        "caret": Position(
                            file="06-e1005.c",
                            line=1,
                            display_column=1,
                            byte_column=1,
                            column=1,
                        ),
                        "finish": Position(
                            file="06-e1005.c",
                            line=1,
                            display_column=3,
                            byte_column=3,
                            column=3,
                        ),
                    }
                ],
                message="expected declaration or statement at end of input",
                children=[],
                column_origin=1,
                escape_source=False,
            )
        ],
    ),
    (
        b"[{\"kind\": \"error\", \"message\": \"expected '=', ',', ';', 'asm' or "
        b'\'__attribute__\' before \'<\' token", "children": [], "column-origin": '
        b'1, "locations": [{"caret": {"file": "08-e1006.c", "line": 1, "display-co'
        b'lumn": 9, "byte-column": 9, "column": 9}}], "escape-source": false}]\n',
        [
            GCCDiagnostic(
                kind="error",
                option=None,
                locations=[
                    {
                        "caret": Position(
                            file="08-e1006.c",
                            line=1,
                            display_column=9,
                            byte_column=9,
                            column=9,
                        )
                    }
                ],
                message="expected '=', ',', ';', 'asm' or '__attribute__' "
                "before '<' token",
                children=[],
                column_origin=1,
                escape_source=False,
            )
        ],
    ),
    (
        b'[{"kind": "error", "message": "expected declaration specifiers before \'i'
        b'f\'", "children": [], "column-origin": 1, "locations": [{"caret": {"file"'
        b': "18-e1034.c", "line": 2, "display-column": 5, "byte-column": 5, "colum'
        b'n": 5}, "finish": {"file": "18-e1034.c", "line": 2, "display-column": 6,'
        b' "byte-column": 6, "column": 6}}], "escape-source": false}, {"kind": "er'
        b'ror", "message": "expected \'{\' at end of input", "children": [], "column'
        b'-origin": 1, "locations": [{"caret": {"file": "18-e1034.c", "line": 4, "'
        b'display-column": -1, "byte-column": -1, "column": -1}}], "escape-source"'
        b": false}]\n",
        [
            GCCDiagnostic(
                kind="error",
                option=None,
                locations=[
                    {
                        "caret": Position(
                            file="18-e1034.c",
                            line=2,
                            display_column=5,
                            byte_column=5,
                            column=5,
                        ),
                        "finish": Position(
                            file="18-e1034.c",
                            line=2,
                            display_column=6,
                            byte_column=6,
                            column=6,
                        ),
                    }
                ],
                message="expected declaration specifiers before 'if'",
                children=[],
                column_origin=1,
                escape_source=False,
            ),
            GCCDiagnostic(
                kind="error",
                option=None,
                locations=[
                    {
                        "caret": Position(
                            file="18-e1034.c",
                            line=4,
                            display_column=-1,
                            byte_column=-1,
                            column=-1,
                        )
                    }
                ],
                message="expected '{' at end of input",
                children=[],
                column_origin=1,
                escape_source=False,
            ),
        ],
    ),
    (
        b'[{"kind": "error", "message": "conflicting types for \'main\'; have \'int(i'
        b'nt,  char **)\'", "children": [{"kind": "note", "message": "previous decl'
        b'aration of \'main\' with type \'int(void)\'", "locations": [{"caret": {"'
        b'file": "22-e1014.c", "line": 1, "display-column": 5, "byte-column": 5, "'
        b'column": 5}, "finish": {"file": "22-e1014.c", "line": 1, "display-column'
        b'": 8, "byte-column": 8, "column": 8}}], "escape-source": false}], "colum'
        b'n-origin": 1, "locations": [{"caret": {"file": "22-e1014.c", "line": 2, '
        b'"display-column": 5, "byte-column": 5, "column": 5}, "finish": {"file": '
        b'"22-e1014.c", "line": 2, "display-column": 8, "byte-column": 8, "column"'
        b': 8}}], "escape-source": false}]\n',
        [
            GCCDiagnostic(
                kind="error",
                option=None,
                locations=[
                    {
                        "caret": Position(
                            file="22-e1014.c",
                            line=2,
                            display_column=5,
                            byte_column=5,
                            column=5,
                        ),
                        "finish": Position(
                            file="22-e1014.c",
                            line=2,
                            display_column=8,
                            byte_column=8,
                            column=8,
                        ),
                    }
                ],
                message="conflicting types for 'main'; have 'int(int,  char " "**)'",
                children=[
                    GCCDiagnostic(
                        kind="note",
                        option=None,
                        locations=[
                            {
                                "caret": Position(
                                    file="22-e1014.c",
                                    line=1,
                                    display_column=5,
                                    byte_column=5,
                                    column=5,
                                ),
                                "finish": Position(
                                    file="22-e1014.c",
                                    line=1,
                                    display_column=8,
                                    byte_column=8,
                                    column=8,
                                ),
                            }
                        ],
                        message="previous declaration of "
                        "'main' with type 'int(void)'",
                        children=[],
                        column_origin=None,
                        escape_source=False,
                    )
                ],
                column_origin=1,
                escape_source=False,
            )
        ],
    ),
]


@pytest.mark.parametrize("raw, expected", TEST_CASES)
def test_parse(raw, expected):
    assert GCCDiagnostic.from_json_string(raw) == expected
