### 简介

### 和其他项目有什么不同?

1. 项目提供了对RKLLM的进一步封装 (待完善). 你可以选择直接选择使用本项目封装的C-API.
2. 项目使用现代且更native的`pybind11`框架。比`ctypes`更高效.

### 构建

#### CMake 部分

1. **配置 `config.cmake` 文件**：
   - 确定是否需要自动检测 Python 解释器路径，或者手动指定路径。
   - 决定是否生成用于调试 C API 的实例主程序。

2. **构建步骤**：
   - 创建构建目录并进入：
     ```bash
     mkdir build && cd build
     ```
   - 配置 CMake：
     ```bash
     cmake .. -DPYTHON_EXECUTABLE=$(which python3)
     ```
     如果需要手动指定 Python 解释器路径，请替换 `$(which python3)` 为实际的 Python 路径。
   - 构建并安装：
     ```bash
     cmake --build . --target install
     ```

#### pip 部分

1. **生成 Python 包**：
   - 上述 CMake 配置会在 `build` 目录下生成 `dist` 文件夹，其中包含 `pyproject.toml` 文件。

2. **安装 Python 包**：
   - 使用 pip 安装生成的包：
     ```bash
     pip install ./dist
     ```

#### 注意事项

- 确保已安装必要的依赖项，例如 CMake 和 Python 开发工具。
- 如果遇到问题，可以检查 `build` 目录下的日志文件以获取更多信息。