from __future__ import annotations

import ctypes
import subprocess
from pathlib import Path
from tempfile import TemporaryDirectory

from crimes.exceptions import CCompileError
from crimes.gcc_diagnostics import GCCDiagnostic

# This is the GCC that is installed on my machine right now.
# -fdiagnostics-format=json was introduced in GCC 9.x
GCC = "gcc-13"


def compile_and_link(src: str) -> ctypes.CDLL:
    # TODO: save the shared object to __pycache__?
    basename = Path(src).stem
    object_name = f"{basename}.o"
    shared_library = f"{basename}.dylib"

    with TemporaryDirectory() as tmpdir_str:
        tmpdir = Path(tmpdir_str)
        object_path = str(tmpdir / object_name)
        shared_library_path = str(tmpdir / shared_library)

        # Compile with GCC
        status = subprocess.run(
            [
                GCC,
                # Will print diagnostics to stderr as JSON:
                "-fdiagnostics-format=json",
                "-fPIC",
                "-c",
                "-o",
                object_path,
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
        status = subprocess.run(
            [GCC, "-shared", "-o", shared_library_path, object_path],
            capture_output=True,
        )
        if status.returncode != 0:
            raise NotImplementedError("linking failed and I don't know what to do")

        return ctypes.cdll.LoadLibrary(shared_library_path)
