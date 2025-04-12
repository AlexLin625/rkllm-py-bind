### Introduction

### What makes this project different?

1. This project provides further encapsulation of RKLLM (to be improved). You can choose to use the C-API encapsulated by this project directly.
2. The project uses the modern and more native `pybind11` framework, which is more efficient than `ctypes`.

### Build

#### CMake Section

1. **Configure the `config.cmake` file**:
   - Decide whether to automatically detect the Python interpreter path or specify the path manually.
   - Decide whether to generate a sample main program for debugging the C API.

2. **Build Steps**:
   - Create a build directory and navigate into it:
     ```bash
     mkdir build && cd build
     ```
   - Configure CMake:
     ```bash
     cmake .. -DPYTHON_EXECUTABLE=$(which python3)
     ```
     If you need to specify the Python interpreter path manually, replace `$(which python3)` with the actual Python path.
   - Build and install:
     ```bash
     cmake --build . --target install
     ```

#### pip Section

1. **Generate Python Package**:
   - The above CMake configuration will generate a `dist` folder under the `build` directory, which contains the `pyproject.toml` file.

2. **Install Python Package**:
   - Use pip to install the generated package:
     ```bash
     pip install ./dist
     ```

#### Notes

- Ensure that the necessary dependencies, such as CMake and Python development tools, are installed.
- If you encounter any issues, you can check the log files in the `build` directory for more information.

(Translated by ChatGPT-4o)