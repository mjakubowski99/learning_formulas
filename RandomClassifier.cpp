#include "types.hpp"
#include "FormulaClassifier.hpp"
#include "FormulaEvaluator.hpp"
#include "FormulaGenerator.hpp"
#include <vector>
#include <array>

RandomClassifier::RandomClassifier(
    int cycles_count, 
    int formulas_count, 
    int clauses_count, 
    int literals_count
)
{
    this->generator = new FormulaGenerator();
    this->evaluator = new FormulaEvaluator();
    this->cycles_count = cycles_count;
    this->formulas_count = formulas_count;
    this->clauses_count = clauses_count;
    this->literals_count = literals_count;
}

RandomClassifier::fit(Data * data, int classes_count)
{
    int i = 0;
    this->decision_classes = new DecisionClass[classes_count];

    while (i<this->cycles_count) {
        for(int k=0; k<classes_count; k++) {
            this->generator->makeFormulas(this->decision_classes[k], data, this->formulas_count, this->clauses_count, this->literals_count, k);
        }
        
        this->clearWeakestFormulas(data, classes_count);

        if (this->satisfiableFormulasCountGenerated(classes_count)) {
            break;
        }

        i++;
    }
}

float RandomClassifier::score(Data * data, int classes_count)
{
    int max_votes = 0;
    int predicted_class = 0;

    int score=0;
    int all=0;

    for(int i=0; i<classes_count; i++) {
        for(int j=0; j<data[i].rows_count; i++) {
            if (i==this->evaluator->voteForRow()) {
                score++;
            }
        }
        all+=data[i].rows_count;
    }

    return score / (float) all;
}

bool RandomClassifier::satisfiableFormulasCountGenerated(int classes_count)
{
    for(int i=0; i<classes_count; i++) {
        if (!this->decision_classes[i].positive.size() < this->formulas_count/2) {
            return false;
        }
        if (!this->decision_classes[i].negative.size() < this->formulas_count/2) {
            return false;
        }
    }
    return true;
}

void RandomClassifier::clearWeakestFormualas(Data * data, int classes_count)
{
    for(int i=0; i<classes_count; i++){

        auto formula = this->decision_classes[i].positive.begin();
        while (formula != this->decision_classes[i].positive.end()) {
            if (!this->evaluator->positiveFormulaEfficient(data, *formula, i)) {
                this->decision_classes[i].positive.erase(formula++);
            } else {
                ++formula;
            }
        }

        formula = this->decision_classes[i].negative.begin();
        while (formula != this->decision_classes[i].negative.end()) {
            if (!this->evaluator->negativeFormulaEfficient(data, *formula, i)) {
                this->decision_classes[i].negative.erase(formula++);
            } else {
                ++formula;
            }
        }
    }
}