#include "types.hpp"
#include "FormulaEvaluator.hpp"

bool FormulaEvaluator::positiveFormulaEfficient(Data * data, int classes_count, Formula & formula, int class_index)
{
    FormulaScore score;

    for(int i=0; i<classes_count; i++) {
        //Formula should be positive only for cases when belongs to class
        bool formula_positive = (i == class_index);

        score = score+this->score(formula, data, classes_count, i, true);
    }

    return this->formulaEfficient(score);
}

bool FormulaEvaluator::negativeFormulaEfficient(Data * data, int classes_count, Formula & formula, int class_index)
{
    FormulaScore score = this->score(formula, data, classes_count, class_index, false);
    return this->formulaEfficient(score);
}

bool FormulaEvaluator::formulaEfficient(FormulaScore score)
{
    if (score.false_negatives+score.false_positives == 0 ) {
        return score.true_positives + score.true_negatives > 0;
    }
    return (score.true_positives+score.true_negatives) / (float) (score.false_negatives+score.false_negatives) > 2.0;
}

int FormulaEvaluator::voteForRow(DecisionClass * decision_classes, int classes_count, bool * row, int attributes_count)
{
    int max_score = 0;
    int max_index = 0;

    for (int i=0; i<classes_count; i++) {
        int score = 0;
        DecisionClass decision_class = decision_classes[i];

        for(Formula formula : decision_class.positive_formulas) {
            if (this->formulaSatisfied(formula, row, attributes_count)) {
                score++;
            }
        }

        for(Formula formula : decision_class.negative_formulas) {
            if (!this->formulaSatisfied(formula, row, attributes_count)) {
                score++;
            }
        }

        if (score > max_score) {
            max_score = score;
            max_index = i;
        }
    }

    return max_index;
}

FormulaScore FormulaEvaluator::score(Formula formula, Data * data, int classes_count, int class_index, bool expected)
{
    FormulaScore score;

    for(int j=0; j<data[class_index].rows_count; j++) {
        bool formula_satisfied = this->formulaSatisfied(
            formula, 
            data[class_index].data[j],
            data[class_index].attributes_count
        );

        if (expected && formula_satisfied) {
            score.true_positives++;
        }
        else if (expected && !formula_satisfied) {
            score.false_negatives++;
        }
        else if (!expected && !formula_satisfied) {
            score.true_negatives++;
        }
        else {
            score.false_positives++;
        }
    }

    return score;
}

bool FormulaEvaluator::formulaSatisfied(Formula formula, bool * attributes, int attributes_count)
{
    for(Clause clause : formula) {
        bool satisfied = false;

        for(Literal literal : clause) {
            if (attributes[literal.bitPosition] == literal.positive) {
                satisfied = true;
                break;
            }
        }

        if (satisfied != true) {
            return false;
        }
    }
    return true;
}
