"""Code generated from cpp_worker namespace. Please do not edit."""

# ruff: noqa: F821
from typing import NamedTuple, Protocol
from tierkreis.controller.data.models import TKR
from tierkreis.controller.data.types import Struct


class Ansatz(Struct, Protocol):
    a: float
    b: float
    c: float


class gen_inputs(NamedTuple):
    value: TKR[str]

    @staticmethod
    def out() -> type[TKR[Ansatz]]:
        return TKR[Ansatz]

    @property
    def namespace(self) -> str:
        return "cpp_worker"
