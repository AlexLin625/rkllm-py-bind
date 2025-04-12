cmake_minimum_required(VERSION 3.28)
project(rkllm)

set (TARGET_LIB_ARCH aarch64)

# Add pybind project
add_subdirectory(${CMAKE_SOURCE_DIR}/external/pybind11)

file(GLOB SOURCES ${CMAKE_SOURCE_DIR}/src/*.cpp)
pybind11_add_module(rkllm ${SOURCES})
target_include_directories(rkllm PRIVATE ${CMAKE_SOURCE_DIR}/inc)

set(CMAKE_BUILD_TYPE Debug)
target_link_libraries(rkllm PRIVATE "/usr/lib/librkllmrt.so")

add_executable(testllm "test/testMain.cpp")
target_include_directories(testllm PRIVATE ${CMAKE_SOURCE_DIR}/inc)
target_link_libraries(testllm PRIVATE "/usr/lib/librkllmrt.so")

# 安装命令：确保将编译产物和类型定义文件复制到dist/rkllm目录
install(DIRECTORY ${CMAKE_SOURCE_DIR}/python/ DESTINATION ${CMAKE_SOURCE_DIR}/dist/rkllm FILES_MATCHING PATTERN "*.pyi")
install(FILES $<TARGET_FILE:rkllm> DESTINATION ${CMAKE_SOURCE_DIR}/dist/rkllm)