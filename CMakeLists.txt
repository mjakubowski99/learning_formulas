# Minimalne wymagania dla wersji CMake
cmake_minimum_required(VERSION 3.0)

# Nazwa projektu i język
project(learning_formulas)

# Dodanie nagłówków
include_directories(include)

# Ustawienie flag kompilacji dla języka C++
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++11")

# Wskazanie źródeł
set(SOURCES "types.cpp" "utils.cpp" "main.cpp")

# Ustawienie pliku wykonywalnego
add_executable(learning_formulas ${SOURCES})

# Dołączenie biblioteki
#target_link_libraries(learning_formulas ${LIBS})