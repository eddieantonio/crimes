import language_bender.importer
language_bender.importer.install()

# Now we can import our C file:
from hello import hello as hello_from_c  # type: ignore
hello_from_c()
