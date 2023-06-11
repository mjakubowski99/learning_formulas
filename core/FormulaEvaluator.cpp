#include "types.hpp"
#include "FormulaEvaluator.hpp"
#include <iostream>
#include "utils.hpp"

FormulaEvaluator::FormulaEvaluator(float positive_responses_treshold)
{
    this->positive_responses_treshold = positive_responses_treshold;
}

bool FormulaEvaluator::formulaIsEfficient(Data * data, int classes_count, Formula & formula, int class_index)
{
    FormulaScore score;

    for(int i=0; i<classes_count; i++) {
        //Formula should be positive only for cases when belongs to class
        bool formula_positive = (i == class_index);
        score = score+this->score(formula, data, classes_count, i, formula_positive);
    }
    float positive_responses = score.true_positives/(float) data[class_index].rows_count;

    return this->formulaEfficient(score) && positive_responses>this->positive_responses_treshold;
}

bool FormulaEvaluator::formulaEfficient(FormulaScore score)
{
    if (score.false_negatives+score.false_positives == 0 ) {
        return score.true_positives + score.true_negatives > 0;
    }
    return (score.true_positives+score.true_negatives) / (float) (score.false_negatives+score.false_positives) > 2.0;
}

int FormulaEvaluator::voteForRow(std::list<Formula> * decision_class_formulas, int classes_count, Data data, int row, int attributes_count)
{
    int max_score = 0;
    int max_index = 0;

    for (int i=0; i<classes_count; i++) {
        int score = 0;
        
        for(Formula formula : decision_class_formulas[i]) {
            bool satisfied = this->formulaSatisfied(formula, data, row, attributes_count);

            if (satisfied) {
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

float FormulaEvaluator::numericScore(Formula formula, Data * data, int classes_count, int goal)
{
    int total_rows_count = 0;
    int valid_responses_count = 0;
    float result;

    for(int i=0; i<classes_count; i++) {
        total_rows_count += data[i].rows_count;

        for(int j=0; j<data[i].rows_count; j++) {
            bool formula_satisfied = this->formulaSatisfied(
                formula, 
                data[i],
                j,
                data[i].attributes_count
            );

            bool expected = i==goal;

            if (expected==formula_satisfied) {
                valid_responses_count++;
            }
        }
    }

    return valid_responses_count/(float)total_rows_count;
}

FormulaScore FormulaEvaluator::score(Formula formula, Data * data, int classes_count, int class_index, bool expected)
{
    FormulaScore score;

    for(int j=0; j<data[class_index].rows_count; j++) {
        bool formula_satisfied = this->formulaSatisfied(
            formula, 
            data[class_index],
            j,
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

bool FormulaEvaluator::formulaSatisfied(Formula formula, Data data, int row, int attributes_count)
{
    for(Clause clause : formula) {
        bool satisfied = false;

        for(Literal literal : clause) {
            if (data.get(row,literal.bitPosition) == literal.positive) {
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
