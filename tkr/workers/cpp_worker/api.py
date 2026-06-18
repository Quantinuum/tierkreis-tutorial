"""Code generated from cpp_worker namespace. Please do not edit."""

# ruff: noqa: F821
from typing import NamedTuple
from tierkreis.controller.data.models import TKR


class Ansatz(NamedTuple):
    a: TKR[float]
    b: TKR[float]
    c: TKR[float]


class gen_inputs(NamedTuple):
    value: TKR[str]

    @staticmethod
    def out() -> type[Ansatz]:
        return Ansatz

    @property
    def namespace(self) -> str:
        return "cpp_worker"
