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
            int min_clauses_count, 
            int max_clauses_count,
            int min_literals_count,
            int max_literals_count, 
            int goal
        );

        void makePositiveFormulas(
            std::list<Formula> & positive_formulas,
            Data data,
            int formulas_count, 
            int min_clauses_count, 
            int max_clauses_count,
            int min_literals_count,
            int max_literals_count
        );

        void makeNegativeFormulas(
            std::list<Formula> & negative_formulas,
            Data * data,
            int goal,
            int classes_count,
            int formulas_count, 
            int min_clauses_count, 
            int max_clauses_count,
            int min_literals_count,
            int max_literals_count
        );

        int randomIndex(int min, int max, std::set<int> & drawn);
};