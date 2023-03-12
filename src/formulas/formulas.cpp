#include "formulas/formulas.hpp"
#include <iostream>
#include <vector>

bool evaluateFormula(std::map<int, Dataframe> & data, Formula formula, bool vote_for_true)
{
    FormulaScore score = getScore(data[0], formula, vote_for_true);
    int TP = score.true_positives;
    int FN = score.false_negatives;
    int FP = score.false_positives;
    int TN = score.true_negatives;

    score = getScore(data[1], formula, vote_for_true);
    TP += score.true_positives;
    FN += score.false_negatives;
    FP += score.false_positives;
    TN += score.true_negatives;

    if (FP+FN == 0) {
        return true;
    }

    return (TP+TN) / (FP+FN) > 2;
}

FormulaScore getScoreForRow(Row row, std::list<Formula> & formulas, bool goal)
{
    FormulaScore score;

    score.true_positives = 0;
    score.true_negatives = 0;
    score.false_negatives = 0;
    score.false_positives = 0;

    for(Formula formula : formulas) {
        bool satisfied = isFormulaSatisfied(row, formula);

        if (satisfied && goal) {
            score.true_positives++;
        } else if(!satisfied && goal) {
            score.false_negatives++;
        } else if(!satisfied && !goal) {
            score.true_negatives++;
        } else {
            score.false_positives++;
        }
    }

    return score;
}

FormulaScore getScore(Dataframe & data, Formula formula, bool goal)
{
    FormulaScore score;

    score.true_positives = 0;
    score.true_negatives = 0;
    score.false_negatives = 0;
    score.false_positives = 0;

    for(Row row : data) {
        bool satisfied = isFormulaSatisfied(row, formula);

        if (satisfied && goal) {
            score.true_positives++;
        } else if(!satisfied && goal) {
            score.false_negatives++;
        } else if(!satisfied && !goal) {
            score.true_negatives++;
        } else {
            score.false_positives++;
        }
    }

    return score;
}

bool isFormulaSatisfied(Row row, Formula formula)
{
    for(Clause clause : formula) {
        bool satisfied = false;

        for(Literal literal : clause) {
            if (row[literal.bitPosition] == literal.positive) {
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


void displayFormula(Formula formula)
{
    for(Clause clause : formula) {
        std::cout << "(";
        for(Literal literal : clause) {
            displayLiteral(literal);
            std::cout << " v ";
        }
        std::cout << ") ^ \n";
    }
}

void displayLiteral(Literal literal) {
    if (!literal.positive) {
        std::cout << "~";
    }
    std::cout << "X" << literal.bitPosition;
}