from __future__ import annotations

import sys
from ctypes import CDLL
from importlib.machinery import ModuleSpec
from types import ModuleType
from importlib.abc import MetaPathFinder, Loader
from typing import Sequence, Optional
from pathlib import Path

from language_bender.unorganized import compile_and_run


class CDLLModule(ModuleType):
    __src_path__: str
    __cdll__: CDLL | None

    def __init__(self, name: str, src_path: str):
        # Initialize this first to prevent fruitless recursive getattr() calls
        self.__cdll__: CDLL | None = None
        super().__init__(name)
        self.__src_path__ = src_path

    def __getattr__(self, name):
        if self.__cdll__ is not None:
            return getattr(self.__cdll__, name)
        raise AttributeError(name)


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
        # Pass both the name and the source code path so that exec_module knows where to find the source code.
        module = CDLLModule(spec.name, spec.loader_state['path'])
        return module

    def exec_module(self, module: ModuleType) -> None:
        cdll = compile_and_run(str(module.__src_path__))
        module.__cdll__ = cdll


# Insert our Importer before all the others.
sys.meta_path.insert(0, CFinder())

# Now we can import our C file:
from hello import hello as hello_from_c  # type: ignore
hello_from_c()
