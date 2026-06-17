# TODO Implement your custom worker here.
from tierkreis import Worker
from pytket import Circuit
from sympy import Symbol
from pytket.pauli import QubitPauliString
from pytket.utils.measurements import (
    append_pauli_measurement as append_pauli_measurement_impl,
)
from pytket.transform import Transform

worker = Worker("old_worker")


@worker.task()
def substitute(circuit: Circuit, a: float, b: float, c: float) -> Circuit:
    circuit.symbol_substitution({Symbol("a"): a, Symbol("b"): b, Symbol("c"): c})
    return circuit


@worker.task()
def append_pauli_measurement(
    circuit: Circuit,
    pauli_string: QubitPauliString,
) -> Circuit:
    append_pauli_measurement_impl(pauli_string, circuit)
    return circuit


@worker.task()
def optimise_ansatz(circuit: Circuit) -> Circuit:
    Transform.OptimisePhaseGadgets().apply(circuit)
    return circuit
