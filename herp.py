import sys
import traceback
from pathlib import Path
from types import TracebackType

import language_bender
from language_bender.exceptions import CCompileError

language_bender.install()

original_except_hook = sys.excepthook


def special_excepthook(
    exception_type: type[BaseException],
    exception_value: BaseException,
    tb: TracebackType | None,
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

    # line = path.read_text().splitlines()[position.line - 1]
    fake_frame = traceback.FrameSummary(
        filename=position.file,
        lineno=position.line,
        name=path.name,
        # line=line
        colno=position.column - 1,
        end_lineno=end_position.line,
        end_colno=end_position.column,
    )
    summary.append(fake_frame)

    for line in summary.format():
        print(line, end="", file=sys.stderr)
    te = traceback.TracebackException(
        exception_type, exception_value, None, compact=True
    )
    for line in te.format_exception_only():
        print(line, end="", file=sys.stderr)

    # traceback.print_exception(exception_type, exception_value, tb)

    # # Outer traceback
    # summary = traceback.extract_stack(tb.tb_frame)
    # if tb.tb_next is not None:
    #     # Inner traceback
    #     summary += traceback.extract_stack(tb.tb_next.tb_frame)
    # breakpoint()


sys.excepthook = special_excepthook


# Now we can import our C file:
from libhello import hello  # type: ignore

hello()
