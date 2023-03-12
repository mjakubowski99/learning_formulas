# Minimalne wymagania dla wersji CMake
cmake_minimum_required(VERSION 3.0)

# Nazwa projektu i język
project(learning_formulas)

# Dodanie nagłówków
include_directories(../include)

# Ustawienie flag kompilacji dla języka C++
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++11")

# Wskazanie źródeł
set(SOURCES "../tests/formulas.cpp")
file(GLOB SOURCES_FORMULAS "../src/formulas/*.cpp ")
file(GLOB SOURCES_EVALUATORS "../src/evaluators/*.cpp ")

# Ustawienie pliku wykonywalnego
add_executable(learning_formulas ${SOURCES_FORMULAS} ${SOURCES_EVALUATORS} ${SOURCES})