#include "types.hpp"
#include <set>

class FormulaGenerator {
    public:
        void makeFormulas(
            DecisionClass & decision_class, 
            Data * data, 
            int classes_count, 
            int formulas_count, 
            int clauses_count, 
            int literals_count, 
            int goal
        );

        void makePositiveFormulas(
            DecisionClass & decision_class, 
            Data data,
            int formulas_count, 
            int clauses_count, 
            int literals_count
        );

        void makeNegativeFormulas(
            DecisionClass & decision_class, 
            Data data,
            int formulas_count, 
            int clauses_count, 
            int literals_count
        );

        int randomIndex(int min, int max, std::set<int> & drawn);
};