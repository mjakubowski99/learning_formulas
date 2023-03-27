#define CATCH_CONFIG_MAIN
#include <catch2/catch.hpp>
#include <vector>
#include "../types.hpp"
#include "../FormulaGenerator.hpp"
#include "../FormulaEvaluator.hpp"
#include "../utils.hpp"
#include <list>
using namespace std;

TEST_CASE("Formula generator generate formula") {
    //Given
    FormulaGenerator generator;
    DecisionClass decision_class;
    decision_class.class_index = 0;
    vector<vector<bool>> test_data {
        {true, false, false, false, true},
        {false, false, false, false, true},
        {false, false, false, false, true},
        {false, false, false, false, true}
    };
    Data data1(4, 5);
    data1.fromVector(test_data);
    Data data2(4, 5);
    data2.fromVector(test_data);
    int classes_count = 2;
    int formulas_count = 4;
    int clauses_count = 2;
    int literals_count = 2;

    Data * datas = new Data[2] {data1, data2};

    //When
    list<Formula> formulas = generator.makeFormulas(datas, classes_count, formulas_count, clauses_count, literals_count, 0);

    //Then
    REQUIRE(formulas_count.size() == formulas_count);
}

TEST_CASE("Formula evaluator correctly evaluate positive formula") {
    std::vector<std::vector<bool>> test_data {
        {false, true, false, false, true},
        {false, true, false, false, true},
        {false, true, false, false, true},
        {false, false, false, false, false}
    };

    FormulaEvaluator evaluator;
    Data data(4, 5);
    data.fromVector(test_data);

    Data * d = new Data[1];
    d[0] = data;

    Formula formula = fromString("(X0vX1)^(X4vX3");

    REQUIRE(evaluator.formulaIsEfficient(d, 1, formula, 0) == true);
}