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
            int goal,
            bool constant_size=true
        );

        void makePositiveFormulas(
            std::list<Formula> & positive_formulas,
            Data data,
            int formulas_count, 
            int clauses_count, 
            int literals_count,
            bool constant_size
        );

        void makeNegativeFormulas(
            std::list<Formula> & negative_formulas,
            Data * data,
            int goal,
            int classes_count,
            int formulas_count, 
            int clauses_count, 
            int literals_count,
            bool constant_size
        );

        int randomIndex(int min, int max, std::set<int> & drawn);
};