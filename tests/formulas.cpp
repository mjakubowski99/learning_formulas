#define CATCH_CONFIG_MAIN
#include "formulas/formulas.hpp"
#include "formulas/generator.hpp"
#include <catch2/catch.hpp>
#include <vector>

TEST_CASE("Formula (x1 V x2) ^ (x3 V x4) satisfiable by x1=true,x2=false,x3=false,x4=true") {
    Literal literal1(1, true);
    Literal literal2(2, true);
    Literal literal3(3, true);
    Literal literal4(4, true);

    Clause clause1;
    clause1.push_back(literal1);
    clause1.push_back(literal2);

    Clause clause2;
    clause2.push_back(literal3);
    clause2.push_back(literal4);

    Formula formula;
    formula.push_back(clause1);
    formula.push_back(clause2);

    Row row = new bool[4]{true, false, true, true};

    REQUIRE(isFormulaSatisfied(row, formula) == true);
}

TEST_CASE("Formula generator generate formula") {
    int rows = 1000;
    int cols = 100;
    int formulas_count = 100;
    int clauses_count = 10;
    int literals_count = 10;

    Dataframe dataframe = new Row[rows];
    for(int i=0; i<rows; i++){
        Row row = new bool[cols];
        for(int j=0; j<cols; j++) {
            row[j] = j%2==0;
        }
        dataframe[i] = row;
    }
    
    Formula * formulas = generateNegativeFormulas(dataframe, rows, cols, formulas_count, clauses_count, literals_count);

    REQUIRE(formulas[0].size() == clauses_count);
    REQUIRE(formulas[0][0].size() == literals_count);
}