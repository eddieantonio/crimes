from __future__ import annotations

import ctypes
import json
import subprocess
from pathlib import Path

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


def compile_and_run(src):
    # TODO: save the object file to some tmp dir?
    # TODO: save the shared object to __pycache__?
    basename = Path(src).stem
    status = subprocess.run(
        [
            "gcc-13",
            "-fdiagnostics-format=json",
            "-fPIC",
            "-c",
            "-o",
            f"{basename}.o",
            src,
        ],
        capture_output=True,
    )
    pems = GCCDiagnostic.from_json_string(status.stderr)
    if pems:
        assert status.returncode != 0
        print_as_python(pems[0])
        # TODO: this should raise a SyntaxError/ImportError, whichever is more relevant
    assert status.returncode == 0

    # Now link
    # TODO: use distutils.ccompiler?
    # TODO: make this platform independent -- that could be done with distutils?
    status = subprocess.run(
        ["gcc-13", "-shared", "-o", f"lib{basename}.dylib", f"{basename}.o"],
        capture_output=True,
    )
    if status.returncode != 0:
        raise NotImplementedError("linking failed and I don't know what to do")

    libhello = ctypes.cdll.LoadLibrary(f"./lib{basename}.dylib")
    return libhello


if __name__ == "__main__":
    libhello = compile_and_run("hello.c")
    libhello.hello()