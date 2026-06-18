from pathlib import Path
from tierkreis.namespace import Namespace


if __name__ == "__main__":
    namespace = Namespace.from_spec_file(Path(__file__).parent / "api.tsp")
    namespace.name = "cpp_worker"
    namespace.write_stubs(Path(__file__).parent / "api.py")
