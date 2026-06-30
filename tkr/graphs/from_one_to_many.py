import logging
from typing import Any, NamedTuple
from uuid import UUID

from cpp_worker import gen_inputs, Ansatz
from guppylang import guppy
from guppylang.std.angles import angle
from guppylang.std.builtins import array
from guppylang.std.quantum import cx, qubit, rz
from pytket import Qubit
from pytket.pauli import Pauli, QubitPauliString
from tierkreis.builder import Graph
from tierkreis.controller import run_graph
from tierkreis.executor import ShellExecutor
from tierkreis.models import OpaqueType, TKR, Workflow
from tierkreis.storage import FileStorage, read_outputs


from guppy_main import (
    hamiltonian_sim as old_sim,
    SymbolicExecutionInputs as OldSymbolicExecutionInputs,
)


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


class SymbolicExecutionInputs(NamedTuple):
    value: TKR[
        str
    ]  # For demonstration purposes, we use JW as potential input to a cpp library
    ham: TKR[list[tuple[OpaqueType["pytket._tket.pauli.QubitPauliString"], float]]]
    ansatz: TKR[OpaqueType["hugr.package.Package"]]


def hamiltonian_sim() -> Workflow[SymbolicExecutionInputs, TKR[float]]:
    simulation_graph = Graph(SymbolicExecutionInputs, TKR[float])
    ansatz_inputs: Ansatz = simulation_graph.task(
        gen_inputs(simulation_graph.inputs.value)
    )

    embedded = simulation_graph.embed(
        old_sim(),
        OldSymbolicExecutionInputs(
            ansatz_inputs.a,
            ansatz_inputs.b,
            ansatz_inputs.c,
            simulation_graph.inputs.ham,
            simulation_graph.inputs.ansatz,
        ),
        TKR[float],
    )

    return simulation_graph.finish_with_outputs(embedded)


class MultipleHamiltoniansInputs(NamedTuple):
    value: TKR[str]
    hamiltonians: TKR[
        list[list[tuple[OpaqueType["pytket._tket.pauli.QubitPauliString"], float]]]
    ]
    ansatz: TKR[OpaqueType["hugr.package.Package"]]


def multiple_hamiltonian_sim() -> Workflow[
    MultipleHamiltoniansInputs, TKR[list[float]]
]:
    simulation_graph = Graph(MultipleHamiltoniansInputs, TKR[list[float]])
    map_inputs = simulation_graph.map(
        lambda x: SymbolicExecutionInputs(
            simulation_graph.inputs.value, x, simulation_graph.inputs.ansatz
        ),
        simulation_graph.inputs.hamiltonians,
    )
    exp_values = simulation_graph.map(hamiltonian_sim(), map_inputs)

    return simulation_graph.finish_with_outputs(exp_values)


def inputs() -> dict[str, Any]:
    ansatz_package = guppy.library(ansatz).compile()
    qubits = [Qubit(0), Qubit(1), Qubit(2), Qubit(3)]
    hamiltonians = [
        [
            (
                QubitPauliString(
                    qubits, [Pauli.X, Pauli.Y, Pauli.X, Pauli.I]
                ).to_list(),
                0.1,
            ),
            (
                QubitPauliString(
                    qubits, [Pauli.Y, Pauli.Z, Pauli.X, Pauli.Z]
                ).to_list(),
                0.5,
            ),
            (
                QubitPauliString(
                    qubits, [Pauli.X, Pauli.Y, Pauli.Z, Pauli.I]
                ).to_list(),
                0.3,
            ),
            (
                QubitPauliString(
                    qubits, [Pauli.Z, Pauli.Y, Pauli.X, Pauli.Y]
                ).to_list(),
                0.6,
            ),
        ],
        [
            (
                QubitPauliString(
                    qubits, [Pauli.X, Pauli.Y, Pauli.X, Pauli.I]
                ).to_list(),
                0.2,
            ),
            (
                QubitPauliString(
                    qubits, [Pauli.Y, Pauli.Z, Pauli.X, Pauli.Z]
                ).to_list(),
                0.4,
            ),
            (
                QubitPauliString(
                    qubits, [Pauli.X, Pauli.Y, Pauli.Z, Pauli.I]
                ).to_list(),
                0.4,
            ),
            (
                QubitPauliString(
                    qubits, [Pauli.Z, Pauli.Y, Pauli.X, Pauli.Y]
                ).to_list(),
                0.5,
            ),
        ],
    ]
    return {
        "ansatz": ansatz_package,
        "hamiltonians": hamiltonians,
        "value": "JW",
    }


def main() -> None:
    graph = multiple_hamiltonian_sim()
    storage = FileStorage(workflow_id=UUID(int=12348), name="hamiltonian_simulation")
    executor = ShellExecutor(None, storage.workflow_dir)
    storage.clean_graph_files()
    run_graph(storage, executor, graph, inputs())
    # storage = debug_graph(graph, inputs())
    result = read_outputs(graph, storage)
    print("Value is: ", result)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()
