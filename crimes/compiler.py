from __future__ import annotations

import ctypes
import os
import subprocess
from functools import cache
from pathlib import Path
from tempfile import TemporaryDirectory

from crimes.exceptions import CCompileError
from crimes.gcc_diagnostics import GCCDiagnostic


def compile_and_link(src: str) -> ctypes.CDLL:
    # TODO: save the shared object to __pycache__?
    basename = Path(src).stem
    object_name = f"{basename}.o"
    shared_library = f"{basename}.dylib"

    with TemporaryDirectory() as tmpdir_str:
        tmpdir = Path(tmpdir_str)
        object_path = str(tmpdir / object_name)
        shared_library_path = str(tmpdir / shared_library)

        # Compile with a compatible compiler
        status = subprocess.run(
            [
                _compiler(),
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
            [_linker(), "-shared", "-o", shared_library_path, object_path],
            capture_output=True,
        )
        if status.returncode != 0:
            raise NotImplementedError("linking failed and I don't know what to do")

        return ctypes.cdll.LoadLibrary(shared_library_path)


@cache
def _compiler() -> str:
    """
    Returns the command or path to a compiler that supports -fdiagnostics-format=json

    Note: -fdiagnostics-format=json was introduced in GCC 9.x
    """
    cc = os.getenv("CC", "cc")

    # Let's try a sample compile with -fdiagnostics-format=json
    try:
        status = subprocess.run(
            [cc, "-fdiagnostics-format=json", "-c", "-x", "c", "/dev/null"],
            capture_output=True,
            check=True,
        )
    except subprocess.CalledProcessError:
        raise NotImplementedError(
            f"Unfortunately, the compiler I found ({cc}) cannot be used to commit crimes.\n"
            "Please use gcc version 9.0 or greater.\n"
            "If a recent version of gcc is installed on your system, but not detected,\n"
            "try setting the CC environment variable before running this program \n"
            "For example:\n"
            " $ env CC=gcc-13 python3 myprogram.py"
        )
    assert status.stderr.startswith(b"[")
    assert status.stderr.rstrip().endswith(b"]")

    return cc


def _linker() -> str:
    return _compiler()
