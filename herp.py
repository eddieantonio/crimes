import language_bender.autoinstall

# isort: split

# Now we can import our C file:
from libhello import hello  # type: ignore

hello()
