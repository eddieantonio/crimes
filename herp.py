from __future__ import annotations

import sys

from language_bender.importer import CFinder

# Insert our Importer before all the others.
sys.meta_path.insert(0, CFinder())

# Now we can import our C file:
from hello import hello as hello_from_c  # type: ignore
hello_from_c()
