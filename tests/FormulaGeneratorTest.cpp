#define CATCH_CONFIG_MAIN
#include <catch2/catch.hpp>
#include <vector>
#include "../types.hpp"
#include "../FormulaGenerator.hpp"
#include "../utils.hpp"
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
    generator.makeFormulas(decision_class, datas, classes_count, formulas_count, clauses_count, literals_count, 0);

    std::cout << stringifyFormula(*decision_class.positive_formulas.begin());

    //Then
    REQUIRE(decision_class.positive_formulas.size() == 2);
    REQUIRE(decision_class.negative_formulas.size() == 2);
}