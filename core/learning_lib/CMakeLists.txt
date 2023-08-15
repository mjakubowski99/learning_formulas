cmake_minimum_required(VERSION 3.10)

project(formulas_learning_lib)

add_library(formulas_learning_lib
    Algorithm.cpp 
    FormulaEvaluator.cpp 
    FormulaGenerator.cpp 
    types.cpp 
    utils.cpp
)
