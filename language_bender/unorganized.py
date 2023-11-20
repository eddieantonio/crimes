from __future__ import annotations

import ctypes
import subprocess
from pathlib import Path

from language_bender.exceptions import CCompileError
from language_bender.gcc_diagnostics import GCCDiagnostic

# This is the GCC that is installed on my machine right now.
# -fdiagnostics-format=json was introduced in GCC 9.x
GCC = "gcc-13"


def compile_and_run(src):
    # TODO: save the object file to some tmp dir?
    # TODO: save the shared object to __pycache__?
    basename = Path(src).stem
    object_name = f"{basename}.o"

    # Compile with GCC
    status = subprocess.run(
        [
            GCC,
            # Will print diagnostics to stderr as JSON:
            "-fdiagnostics-format=json",
            "-fPIC",
            "-c",
            "-o",
            object_name,
            src,
        ],
        capture_output=True,
    )

    # Compilation failed
    if status.returncode != 0:
        diagnostics = GCCDiagnostic.from_json_string(status.stderr)
        assert len(diagnostics) >= 1
        error_message = next(e for e in diagnostics if e.kind == "error")
        raise CCompileError(error_message)

    # Now link
    # TODO: use distutils.ccompiler?
    # TODO: make this platform independent -- that could be done with distutils?
    shared_library = f"lib{basename}.dylib"
    status = subprocess.run(
        [GCC, "-shared", "-o", shared_library, object_name],
        capture_output=True,
    )
    if status.returncode != 0:
        raise NotImplementedError("linking failed and I don't know what to do")

    return ctypes.cdll.LoadLibrary(f"./{shared_library}")
