cmake_minimum_required(VERSION 3.18)
project(gpu_testing LANGUAGES CXX CUDA)

# Set C++ and CUDA standards to C++17
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CUDA_STANDARD 17)
set(CMAKE_CUDA_STANDARD_REQUIRED ON)

# Find Python and pybind11 dynamically based on the active environment
find_package(Python 3 REQUIRED COMPONENTS Interpreter Development)
find_package(pybind11 CONFIG REQUIRED)

# Create the pybind11 module target from the CUDA source file
pybind11_add_module(gpu_testing MODULE gpu_testing.cu)

# Include directories
target_include_directories(gpu_testing PRIVATE
    ../../../../CGBN/include/
)

# Link external libraries (-lgmp)
target_link_libraries(gpu_testing PRIVATE gmp)

# Pass compiler flags (-Wall, -Werror) to the host compiler via nvcc
target_compile_options(gpu_testing PRIVATE
    $<$<COMPILE_LANGUAGE:CUDA>:-O3 -Xcompiler=-Wall,-Werror>
    $<$<COMPILE_LANGUAGE:CXX>:-O3,-Wall,-Werror>
)
