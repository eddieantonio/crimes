import language_bender.excepthook

language_bender.install()
language_bender.excepthook.install_excepthook()

# Now we can import our C file:
from libhello import hello  # type: ignore

hello()
