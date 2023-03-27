#pragma once

#include "types.hpp"

class FormulaEvaluator {
    public:
        bool formulaIsEfficient(Data * data, int classes_count, Formula & formula, int class_index);

        int voteForRow(std::list<Formula> * decision_class_formulas, int classes_count, bool * row, int attributes_count);

        FormulaScore score(Formula formula, Data * data, int classes_count, int class_index, bool expected);

        bool formulaEfficient(FormulaScore score);

        bool formulaSatisfied(Formula formula, bool * attributes, int attributes_count);
};