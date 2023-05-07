#include "types.hpp"
#include "FormulaEvaluator.hpp"
#include <iostream>

bool FormulaEvaluator::formulaIsEfficient(Data * data, int classes_count, Formula & formula, int class_index)
{
    FormulaScore score;

    for(int i=0; i<classes_count; i++) {
        //Formula should be positive only for cases when belongs to class
        bool formula_positive = (i == class_index);
        score = score+this->score(formula, data, classes_count, i, formula_positive);
    }
    float positive_responses = score.true_positives/(float) data[class_index].rows_count;

    return this->formulaEfficient(score) && positive_responses>0.7;
}

bool FormulaEvaluator::formulaEfficient(FormulaScore score)
{
    if (score.false_negatives+score.false_positives == 0 ) {
        return score.true_positives + score.true_negatives > 0;
    }
    return (score.true_positives+score.true_negatives) / (float) (score.false_negatives+score.false_positives) > 2.0;
}

int FormulaEvaluator::voteForRow(std::list<Formula> * decision_class_formulas, int classes_count, bool * row, int attributes_count)
{
    int max_score = 0;
    int max_index = 0;

    for (int i=0; i<classes_count; i++) {
        int score = 0;
        
        for(Formula formula : decision_class_formulas[i]) {
            if (this->formulaSatisfied(formula, row, attributes_count)) {
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
