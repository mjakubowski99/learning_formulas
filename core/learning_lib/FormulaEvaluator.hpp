#pragma once

#include "types.hpp"

class FormulaEvaluator {
    float positive_responses_treshold;
    public:
        FormulaEvaluator(float positive_responses_treshold);
        
        bool formulaIsEfficient(Data * data, int classes_count, Formula & formula, int class_index);

        int voteForRow(std::list<Formula> * decision_class_formulas, int classes_count, Data data, int row, int attributes_count);

        FormulaScore score(Formula formula, Data * data, int classes_count, int class_index, bool expected);

        float correctnessScore(Formula formula, Data * data, int classes_count, int goal);

        float fMeasureScore(Formula formula, Data * data, int classes_count, int goal);

        bool formulaEfficient(FormulaScore score);

        bool formulaSatisfied(Formula formula, Data data, int row, int attributes_count);
};