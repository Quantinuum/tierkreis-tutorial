import logging
from typing import Any, NamedTuple
from uuid import UUID

from guppy_worker import emulate, to_backend_result
from guppylang import guppy
from guppylang.std.angles import angle
from guppylang.std.builtins import array
from guppylang.std.quantum import cx, qubit, rz
from new_worker import append_pauli_measurements, optimise_ansatz, substitute
from pytket import Qubit
from pytket.pauli import Pauli, QubitPauliString
from pytket_worker import expectation
from tierkreis.builder import Graph
from tierkreis.builtins import add, times, tkr_zip, untuple, unzip
from tierkreis.controller import run_graph
from tierkreis.controller.storage.debug_graph import debug_graph
from tierkreis.executor import ShellExecutor
from tierkreis.graphs.fold import FoldFunctionInput, FoldGraphInputs, fold_graph
from tierkreis.models import TKR, OpaqueType, Workflow
from tierkreis.storage import FileStorage, read_outputs


@guppy(link_name="ansatz")
def ansatz(qbts: array[qubit, 4], a: float, b: float, c: float) -> None:  # type: ignore
    for i in array(0, 1, 2):
        cx(qbts[i], qbts[i + 1])
    rz(qbts[0], angle(a))
    for i in array(2, 1, 0):
        cx(qbts[i], qbts[i + 1])
    rz(qbts[0], angle(b))
    for i in array(0, 1, 2):
        cx(qbts[i], qbts[i + 1])
    rz(qbts[0], angle(c))
    for i in array(2, 1, 0):
        cx(qbts[i], qbts[i + 1])


class SubmitInputs(NamedTuple):
    circuit: TKR[OpaqueType["hugr.package.Package"]]
    pauli_string: TKR[OpaqueType["pytket._tket.pauli.QubitPauliString"]]
    n_shots: TKR[int]


def exp_val():
    g = Graph(SubmitInputs, TKR[float])

    circuit = g.inputs.circuit
    pauli_string = g.inputs.pauli_string
    n_shots = g.inputs.n_shots

    measurement_circuit = g.task(append_pauli_measurements(circuit, pauli_string))
    compiled_circuit = g.task(optimise_ansatz(measurement_circuit))
    result = g.task(emulate(compiled_circuit, g.const(4), n_shots))
    backend_result = g.task(to_backend_result(result))
    av = g.task(expectation(backend_result))
    return g.finish_with_outputs(av)


ComputeTermsInputs = FoldFunctionInput[
    tuple[float, float], float
]  # (value: (x,y) , accum: z) -> new_accum


def compute_terms():
    g = Graph(ComputeTermsInputs, TKR[float])

    res_0, res_1 = g.task(untuple(g.inputs.value))
    prod = g.task(times(res_0, res_1))
    sum = g.task(add(g.inputs.accum, prod))

    return g.finish_with_outputs(sum)


class SymbolicExecutionInputs(NamedTuple):
    a: TKR[float]
    b: TKR[float]
    c: TKR[float]
    ham: TKR[list[tuple[OpaqueType["pytket._tket.pauli.QubitPauliString"], float]]]
    ansatz: TKR[OpaqueType["hugr.package.Package"]]


def hamiltonian_sim() -> Workflow[SymbolicExecutionInputs, TKR[float]]:
    simulation_graph = Graph(SymbolicExecutionInputs, TKR[float])
    substituted_ansatz = simulation_graph.task(
        substitute(
            simulation_graph.inputs.ansatz,
            simulation_graph.inputs.a,
            simulation_graph.inputs.b,
            simulation_graph.inputs.c,
        )
    )
    pauli_strings_list, parameters_list = simulation_graph.task(
        unzip(simulation_graph.inputs.ham)
    )
    input_circuits = simulation_graph.map(
        lambda x: SubmitInputs(substituted_ansatz, x, simulation_graph.const(100)),
        pauli_strings_list,
    )
    exp_values = simulation_graph.map(exp_val(), input_circuits)
    tuple_values = simulation_graph.task(tkr_zip(exp_values, parameters_list))
    fold_inputs = FoldGraphInputs(simulation_graph.const(0.0), tuple_values)
    computed = simulation_graph.eval(fold_graph(compute_terms()), fold_inputs)
    return simulation_graph.finish_with_outputs(computed)


def inputs() -> dict[str, Any]:
    ansatz_package = guppy.library(ansatz).compile()
    qubits = [Qubit(0), Qubit(1), Qubit(2), Qubit(3)]
    hamiltonian = [
        (QubitPauliString(qubits, [Pauli.X, Pauli.Y, Pauli.X, Pauli.I]).to_list(), 0.1),
        (QubitPauliString(qubits, [Pauli.Y, Pauli.Z, Pauli.X, Pauli.Z]).to_list(), 0.5),
        (QubitPauliString(qubits, [Pauli.X, Pauli.Y, Pauli.Z, Pauli.I]).to_list(), 0.3),
        (QubitPauliString(qubits, [Pauli.Z, Pauli.Y, Pauli.X, Pauli.Y]).to_list(), 0.6),
    ]
    return {
        "ansatz": ansatz_package,
        "a": 0.2,
        "b": 0.55,
        "c": 0.75,
        "ham": hamiltonian,
    }


def main() -> None:
    graph = hamiltonian_sim()
    storage = FileStorage(
        workflow_id=UUID(int=12346), name="guppy_hamiltonian_simulation"
    )
    executor = ShellExecutor(None, storage.workflow_dir)
    storage.clean_graph_files()
    run_graph(storage, executor, graph, inputs())
    # storage = debug_graph(graph, inputs())
    result = read_outputs(graph, storage)
    print("Value is: ", result)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()
