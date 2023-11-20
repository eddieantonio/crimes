import sys
import traceback
from pathlib import Path
from types import TracebackType
from typing import Optional

from language_bender.exceptions import CCompileError

original_except_hook = sys.excepthook


def special_excepthook(
    exception_type: type[BaseException],
    exception_value: BaseException,
    tb: Optional[TracebackType],
) -> None:
    if not isinstance(exception_value, CCompileError):
        return original_except_hook(exception_type, exception_value, tb)

    # Another idea is to use traceback.walk_stack() to yield stack frames
    assert tb is not None
    summary = traceback.extract_tb(tb)
    # summary is in  "Most recent call last" order
    assert len(summary) >= 2

    # Last frame is the thing that raised the compiler error:
    raise_frame = summary.pop()
    assert raise_frame.line is not None
    assert "raise" in raise_frame.line
    assert exception_type.__name__ in raise_frame.line

    # That should have been our frame from importer.py
    while frame := summary.pop():
        if "importlib" not in frame.filename and not frame.filename.endswith(
            "language_bender/importer.py"
        ):
            break

    # We popped one too many frames; put it back:
    summary.append(frame)

    # Okay! We should be left with the stack frame that actually imported the file!
    c_error = exception_value.first_error
    assert c_error.kind == "error"
    assert len(c_error.locations) > 0
    position = c_error.locations[0]["caret"]
    path = Path(position.file)

    end_position = c_error.locations[0].get("finish", position)

    fake_frame = traceback.FrameSummary(
        filename=position.file,
        lineno=position.line,
        name=path.name,
        colno=position.column - 1,
        end_lineno=end_position.line,
        end_colno=end_position.column,
    )
    summary.append(fake_frame)

    # Get Python's internals to print the exception line:
    te = traceback.TracebackException(
        exception_type, exception_value, None, compact=True
    )

    # Everything is ready for printing!
    print("Traceback (most recent call last):", file=sys.stderr)
    for line in summary.format():
        print(line, end="", file=sys.stderr)
    for line in te.format_exception_only():
        print(line, end="", file=sys.stderr)


def install_excepthook():
    sys.excepthook = special_excepthook
