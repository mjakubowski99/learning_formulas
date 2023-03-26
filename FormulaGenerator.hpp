#pragma once

#include "types.hpp"
#include <set>
#include <list>

class FormulaGenerator {
    public:
        std::list<Formula> makeFormulas(
            Data * data, 
            int classes_count, 
            int formulas_count, 
            int clauses_count, 
            int literals_count, 
            int goal
        );

        void makePositiveFormulas(
            std::list<Formula> & positive_formulas,
            Data data,
            int formulas_count, 
            int clauses_count, 
            int literals_count
        );

        void makeNegativeFormulas(
            std::list<Formula> & negative_formulas,
            Data data,
            int formulas_count, 
            int clauses_count, 
            int literals_count
        );

        int randomIndex(int min, int max, std::set<int> & drawn);
};