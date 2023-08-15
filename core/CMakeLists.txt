cmake_minimum_required(VERSION 3.10)

project(learning_formulas)

add_subdirectory(learning_lib)

add_executable(${PROJECT_NAME} main.cpp)

target_link_libraries(${PROJECT_NAME} PUBLIC formulas_learning_lib)

target_include_directories(${PROJECT_NAME} PUBLIC
    "${PROJECT_BINARY_DIR}"
    "${PROJECT_SOURCE_DIR}/learning_lib"
)
