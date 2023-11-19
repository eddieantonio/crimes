"""
Very simple smoke tests for the crimes module.
"""

import sys
from pathlib import Path

import crimes
from crimes.exceptions import CCompileError


import pytest

C_SOURCE_PATH = Path(__file__).parent / 'c-sources'


def test_crimes(commit_crimes, c_sources_on_path):
    """
    Smoke test for the crimes module.
    """

    # Make sure it's on the import path:
    assert (C_SOURCE_PATH / "fib.c").exists()

    from fib import fibonacci
    assert fibonacci(10) == 55


def test_crimes_errors(commit_crimes, c_sources_on_path):
    """
    Test that errors are raised properly.

    This... might depend on the compiler...
    """

    filename = "syntax_error.c"
    assert (C_SOURCE_PATH / filename).exists()

    with pytest.raises(CCompileError) as excinfo:
        from syntax_error import hello

    # the syntax error is on line 4... but it might be detected later
    assert excinfo.value.line >= 4


@pytest.fixture
def commit_crimes():
    """
    crimes.commit() as a pytest fixture.
    """
    with crimes.commit_with_take_backsies():
        yield


@pytest.fixture
def c_sources_on_path():
    """
    Make sure that c-sources/ is in sys.path."
    """
    # Prepend c-sources/ at the very start of the path.
    path = str(C_SOURCE_PATH)
    sys.path.insert(0, path)

    yield

    # Clean up: remove it from the path.
    del sys.path[sys.path.index(path)]


