#include "types.hpp"

class FormulaEvaluator {
    public:
        bool positiveFormulaEfficient(Data * data, int classes_count, Formula & formula, int class_index);

        bool negativeFormulaEfficient(Data * data, int classes_count, Formula & formula, int class_index);

        int voteForRow(DecisionClass * decision_classes, int classes_count, bool * row, int attributes_count);

        FormulaScore score(Formula formula, Data * data, int classes_count, int class_index, bool expected);

        bool formulaEfficient(FormulaScore score);

        bool formulaSatisfied(Formula formula, bool * attributes, int attributes_count);
};