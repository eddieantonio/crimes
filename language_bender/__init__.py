from .importer import install_importer
from .excepthook import install_excepthook


def install():
    """
    Installs all functionality. This includes:
     - importing C files
     - error messages for C files
    """
    install_importer()
    install_excepthook()
