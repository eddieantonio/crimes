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
            # Could not find anything
            return

        return ModuleSpec(name=fullname, loader=self, loader_state={'path': p})

    def create_module(self, spec: ModuleSpec) -> ModuleType:
        module = ModuleType(spec.name)
        module.__src_path__ = spec.loader_state['path']
        return module

    def exec_module(self, module: ModuleType) -> None:
        cdll = compile_and_run(str(module.__src_path__))
        module.__cdll__ = cdll
        module.hello = cdll.hello


sys.meta_path.insert(0, CFinder())

# class CPathFinder(PathEntryFinder):
#     def __init__(self, path: str):
#         breakpoint()
#
#     def find_spec(self, fullname: str, target: ModuleType | None = ...) -> ModuleSpec | None:
#         breakpoint()
#         print(fullname)
#         return None


# del sys.path_importer_cache['/Users/eddie/Programming/language-bender']
# sys.path_hooks.insert(0, lambda path: CPathFinder)

from hello import hello as hello_from_c  # type: ignore
hello_from_c()

#libhello = compile_and_run("hello.c")
#hello = ModuleType("hello")
#hello.hello = libhello.hello
#
#hello.hello()


