from __future__ import annotations

import sys
from importlib.machinery import ModuleSpec
from types import ModuleType
from importlib.abc import MetaPathFinder, Loader
from typing import Sequence
from pathlib import Path

from language_bender.unorganized import compile_and_run


class CFinder(MetaPathFinder, Loader):
    def find_spec(
        self, fullname: str, path: Sequence | None, target: ModuleType | None = ...
    ) -> ModuleSpec | None:

        p = Path(f"{fullname}.c")
        if not p.exists():
            # Could not find the C source code file
            return

        return ModuleSpec(name=fullname, loader=self, loader_state={'path': p})

    def create_module(self, spec: ModuleSpec) -> ModuleType:
        module = ModuleType(spec.name)
        # Place this here so that exec_module knows where to find the source code.
        module.__src_path__ = spec.loader_state['path']
        return module

    def exec_module(self, module: ModuleType) -> None:
        cdll = compile_and_run(str(module.__src_path__))
        module.__cdll__ = cdll
        # TODO: get exported symbols... through nm? through debug symbols?
        module.hello = cdll.hello


# Insert our Importer before all the others.
sys.meta_path.insert(0, CFinder())

# Now we can import our C file:
from hello import hello as hello_from_c  # type: ignore
hello_from_c()
