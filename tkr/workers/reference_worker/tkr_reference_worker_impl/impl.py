"""Reference worker implementation for Tierkreis."""

from guppylang import guppy
from guppylang.std.builtins import array, result
from guppylang.std.angles import angle
from guppylang.std.quantum import collect_measurements, rx, h, measure_array, qubit
from tierkreis import Worker

from hugr.package import Package
from guppylang.std.builtins import comptime
from pytket.pauli import Pauli, QubitPauliString
from tket.passes import NormalizeGuppy


worker = Worker("reference_worker")


@worker.task()
def substitute(
    package: Package, a: float, b: float, c: float, ansatz_name: str = "ansatz"
) -> Package:

    @guppy.declare(link_name=ansatz_name)
    def ansatz_decl(qbts: array[qubit, 4], a: float, b: float, c: float) -> None: ...  # type: ignore

    @guppy(link_name="substituted")
    def substituted(qbts: array[qubit, 4]) -> None:  # type: ignore
        ansatz_decl(qbts, comptime(a), comptime(b), comptime(c))  # type: ignore

    current_package = guppy.library(substituted).compile()
    new_package = package.link(current_package)
    return new_package


@worker.task()
def append_pauli_measurements(
    package: Package, pauli_string: QubitPauliString, ansatz_name: str = "substituted"
) -> Package:

    paulis = [
        (i.index[0], p.value) for i, p in pauli_string.map.items() if p != Pauli.I
    ]

    @guppy.declare(link_name=ansatz_name)
    def ansatz_decl(qbts: array[qubit, 4]) -> None: ...  # type: ignore

    @guppy
    def main() -> None:
        q = array(qubit() for _ in range(4))  # type: ignore
        ansatz_decl(q)  # type: ignore
        for i, p in comptime(paulis):
            if p == 0:
                h(q[i])
            elif p == 1:
                rx(q[i], angle(0.5))  # type: ignore
        # result("counts", measure_array(q)) # Old syntax
        result("counts", collect_measurements(measure_array(q)))  # v1.0.0 syntax

    return main.compile_function().link(package)


@worker.task()
def optimise_ansatz(package: Package) -> Package:
    normalize_pass = NormalizeGuppy()
    normalize_pass(package.modules[0])
    return package
