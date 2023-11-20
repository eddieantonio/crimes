import language_bender

language_bender.install()

# Now we can import our C file:
from libhello import hello  # type: ignore

hello()
