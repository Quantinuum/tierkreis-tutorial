"""Code generated from reference_worker namespace. Please do not edit."""

# ruff: noqa: F821
from typing import NamedTuple
from tierkreis.controller.data.models import TKR, OpaqueType


class substitute(NamedTuple):
    package: TKR[OpaqueType["hugr.package.Package"]]
    a: TKR[float]
    b: TKR[float]
    c: TKR[float]
    ansatz_name: TKR[str] | None = None

    @staticmethod
    def out() -> type[TKR[OpaqueType["hugr.package.Package"]]]:
        return TKR[OpaqueType["hugr.package.Package"]]

    @property
    def namespace(self) -> str:
        return "reference_worker"


class append_pauli_measurements(NamedTuple):
    package: TKR[OpaqueType["hugr.package.Package"]]
    pauli_string: TKR[OpaqueType["pytket._tket.pauli.QubitPauliString"]]
    ansatz_name: TKR[str] | None = None

    @staticmethod
    def out() -> type[TKR[OpaqueType["hugr.package.Package"]]]:
        return TKR[OpaqueType["hugr.package.Package"]]

    @property
    def namespace(self) -> str:
        return "reference_worker"


class optimise_ansatz(NamedTuple):
    package: TKR[OpaqueType["hugr.package.Package"]]

    @staticmethod
    def out() -> type[TKR[OpaqueType["hugr.package.Package"]]]:
        return TKR[OpaqueType["hugr.package.Package"]]

    @property
    def namespace(self) -> str:
        return "reference_worker"
