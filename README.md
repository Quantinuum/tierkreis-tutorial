# Tierkreis Tutorial

This is a tutorial introducing core concepts of the [Tierkreis](https://github.com/Quantinuum/tierkreis) library.
It updates an existing workflow to use the new [guppy](https://guppylang.org) language and to levarage automatic parallelism.

## Setup Instructions

### Prerequisites
- Python >=3.12
- [`uv`](https://docs.astral.sh/uv/#highlights)
- `git`


### Installation

1. Clone and navigate to the project:
   ```bash
   git clone git@github.com:Quantinuum/tierkreis-tutorial.git
   cd tierkreis-tutorial
   ```

2. Set up the development environment:
    ```bash
    uv sync
    ```
3. Make sure the C++ worker binary is in your path:
    ```bash
    export PATH=$PATH:$PWD/workers/cpp_worker
    ```

## Project Structure

```

tkr/                         # Base exercise for the tutorial
├── exercises/               # Learning exercises
│   ├── exercise1.ipynb      # Exercise 1: Implement custom worker
│   └── exercise2.ipynb      # Exercise 2: Extend to multiple Hamiltonians
│
├── graphs/                  # Complete example workflows
│   ├── guppy_main.py        # Single Hamiltonian simulation
│   ├── from_one_to_many.py  # Multiple Hamiltonians with map
│   ├── cpp_guppy_main.py    # C++ worker integration example
│   └── pytket_main.py       # Pytket original example
│
├── material/                # Presentation material
│
└── workers/                 # Worker implementations
    ├── cpp_worker/          # C++ dummy worker
    ├── new_worker/          # New guppy worker (for exercises)
    │   └── tkr_new_worker_impl/
    │       └── impl.py      # TODO: Implementation incomplete
    │
    ├── old_worker/          # Reference implementation
    │
    └── reference_worker/    # Reference implementation

```

## Running Examples

Examples can be run through
```bash
uv run tkr/graphs/<name_of_example>.py
```

## Exercises

### Exercise 1: Implementing a Custom Worker
Complete the `new_worker` implementation and integrate it into the Hamiltonian simulation graph.

[`tkr/exercises/exercise1.ipynb`](tkr/exercises/exercise1.ipynb)

**Tasks:**
1. Implement guppy manipulation functions in `new_worker`
2. Integrate the worker into the graph


### Exercise 2: Scaling to Multiple Hamiltonians
Extend the single Hamiltonian simulation to handle multiple Hamiltonians using `map`.

[`tkr/exercises/exercise2.ipynb`](tkr/exercises/exercise2.ipynb)

**Tasks:**
1. Integrate `cpp_worker` for parameter generation
2. Create a mapping function over multiple Hamiltonians

