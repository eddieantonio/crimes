from __future__ import annotations

import sys
from ctypes import CDLL
from importlib.abc import Loader, MetaPathFinder
from importlib.machinery import ModuleSpec
from pathlib import Path
from types import ModuleType
from typing import Sequence

from language_bender.unorganized import compile_and_run


class CDLLModule(ModuleType):
    __src_path__: str
    __cdll__: CDLL | None

    def __init__(self, name: str, src_path: str):
        # Initialize this first to prevent fruitless recursive getattr() calls
        self.__cdll__: CDLL | None = None
        super().__init__(name)
        self.__file__ = src_path

    def __getattr__(self, name):
        if self.__cdll__ is not None:
            return getattr(self.__cdll__, name)
        raise AttributeError(name)


class CImporter(MetaPathFinder, Loader):
    def find_spec(
        self, fullname: str, path: Sequence | None, target: ModuleType | None = None
    ) -> ModuleSpec | None:
        p = Path(f"{fullname}.c")
        if not p.exists():
            # Could not find the C source code file
            return None

        return ModuleSpec(
            name=fullname, loader=self, loader_state={"path": str(p.resolve())}
        )

    def create_module(self, spec: ModuleSpec) -> CDLLModule:
        # Pass both the name and the source code path so that exec_module knows where to find the source code.
        return CDLLModule(spec.name, spec.loader_state["path"])

    def exec_module(self, module: ModuleType) -> None:
        assert isinstance(module, CDLLModule)
        # TODO: catch CCompileError and do... something!
        cdll = compile_and_run(module.__file__)
        module.__cdll__ = cdll


def install():
    """
    Enable the import of C source code.

    This works by inserting a Finder before all pre-existing finders in sys.meta_path.
    """
    sys.meta_path.insert(0, CImporter())
