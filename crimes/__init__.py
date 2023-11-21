"""
Integrate C into Python.
"""


def install():
    """
    Installs all functionality. This includes:
     - importing C files
     - error messages for C files
    """
    from .excepthook import install_excepthook
    from .importer import install_importer

    install_importer()
    install_excepthook()
