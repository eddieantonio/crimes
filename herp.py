from __future__ import annotations

import ctypes
import json
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Literal, NotRequired, Optional, TypedDict

from language_bender.gcc_diagnostics import GCCDiagnostic


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
