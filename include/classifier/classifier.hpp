#include "types.hpp"
#include "formulas/formulas.hpp"
#include <map>
#include <list>

#ifndef group_hpp
#define group_hpp
struct Group {
    int rows;
    int cols;
    Dataframe dataframe;
};
#endif

#ifndef classifier_hpp
#define classifier_hpp

class Classifier {
    FormulaVote positive_formulas;
    FormulaVote negative_formulas;
    int cycles_limit;
    int expected_formulas_number;
    int expetected_clauses_count;
    int expected_literals_count;

    public:
        Classifier(int cycles_limit, int expected_formulas_number, int expected_clauses_count, int expected_literals_count);

        void fit(std::map<int, Dataframe> data);

        float score(std::map<int, Dataframe> data);
};

#endif