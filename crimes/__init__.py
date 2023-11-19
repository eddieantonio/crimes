"""
Integrate C into Python.
"""

import sys
from contextlib import contextmanager

__ALL__ = ['commit', 'commit_with_take_backsies']


def commit():
    """
    Enables all functionalities of this library. This includes:
     - importing C files
     - error messages for C files
    """
    # Imported here so that there are no side effects for importing the main package.
    from .excepthook import install_excepthook
    from .importer import install_importer

    install_importer()
    install_excepthook()


@contextmanager
def commit_with_take_backsies():
    """
    A context manager that acts like `commit()` but attempts to undo this later.
    """
    from .importer import install_importer, uninstall_importer
    from .excepthook import install_excepthook

    # commit crimes
    importer = install_importer()
    original_excepthook = install_excepthook()

    yield

    # "it was just a prank, bro"
    uninstall_importer(importer)
    sys.excepthook = original_excepthook
