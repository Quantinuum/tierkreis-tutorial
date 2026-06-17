# TODO Implement the Hamiltonian ansatz
from hugr.package import Package
from pytket.pauli import QubitPauliString
from tierkreis import Worker

worker = Worker("new_worker")


@worker.task()
def substitute(
    package: Package, a: float, b: float, c: float, ansatz_name: str = "ansatz"
) -> Package:
    # TODO: Implement the parameter substitution logic here.
    # Some useful hints:
    # - You can forward declare guppy functions like this:
    # @guppy.declare(link_name=ansatz_name)
    # def ansatz_decl(qbts: array[qubit, 4], a: float, b: float, c: float) -> None: ...  # type: ignore
    # - Library functions can be given a link_name to be used in the linking process
    # - also look at guppy.library and Package.link
    ...


@worker.task()
def append_pauli_measurements(
    package: Package, pauli_string: QubitPauliString, ansatz_name: str = "substituted"
) -> Package:
    # TODO: Implement the logic to append Pauli measurements to the ansatz.
    # Some useful hints:
    # - Convert the pauli string into a guppy compatible type
    # - Use guppy constructs to build the measurement circuit
    # - compile_function() and link() might be useful here
    ...


@worker.task()
def optimise_ansatz(package: Package) -> Package:
    # TODO: Implement the ansatz optimization logic here.
    # We want to implement GuppyNormalization
    ...
