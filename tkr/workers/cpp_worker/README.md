# Install

## C++ project

Regular cmake install:
```
mkdir build && cd build
cmake ..
make install
```

make sure the generated `tkr-cpp-worker` binary is in your `$PATH`.

## API

You can use the `generate_stubs.py` script to generate the worker python api from the type spec.
```
uv run generate_stubs.py
```
