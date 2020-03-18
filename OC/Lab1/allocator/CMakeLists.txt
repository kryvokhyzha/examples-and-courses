cmake_minimum_required(VERSION 3.15)
project(allocator)

set(CMAKE_CXX_STANDARD 14)

add_executable(allocator main.cpp mem_alloc.h mem_alloc.cpp)