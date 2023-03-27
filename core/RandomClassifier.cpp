#include "types.hpp"
#include "FormulaEvaluator.hpp"
#include "FormulaGenerator.hpp"
#include "RandomClassifier.hpp"
#include <vector>
#include <array>
#include <iostream>
#include "utils.hpp"
#include <fstream>

RandomClassifier::RandomClassifier(int decision_classes_count, int cycles_count, int formulas_count, int clauses_count, int literals_count)
{
    this->generator = new FormulaGenerator();
    this->evaluator = new FormulaEvaluator();
    this->decision_classes_count = decision_classes_count;
    this->decision_class_formulas = new std::list<Formula>[decision_classes_count];
    this->cycles_count = cycles_count;
    this->formulas_count = formulas_count;
    this->clauses_count = clauses_count;
    this->literals_count = literals_count;
}

void RandomClassifier::fit(Data * data)
{
    int i = 0;

    while (i<this->cycles_count) {
        for(int k=0; k<this->decision_classes_count; k++) {
            int formulas_number = this->formulas_count - this->decision_class_formulas[k].size();

            std::list<Formula> formulas = this->generator->makeFormulas(
                data,
                this->decision_classes_count,
                formulas_number, 
                this->clauses_count, 
                this->literals_count, 
                k
            );

            this->clearWeakestFormulas(formulas, data, k);

            for(Formula formula : formulas) {
                this->decision_class_formulas[k].push_back(formula);
            }

            std::cout << "Formulas for class: " << k << " size: " << this->decision_class_formulas[k].size() << std::endl;
        }

        if (this->satisfiableFormulasCountGenerated()) {
            break;
        }

        i++;
    }
}

float RandomClassifier::score(Data * data)
{
    int max_votes = 0;
    int predicted_class = 0;

    int score=0;
    int all=0;

    for(int i=0; i<this->decision_classes_count; i++) {
        for(int j=0; j<data[i].rows_count; j++) {
            int vote_result = this->evaluator->voteForRow(
                this->decision_class_formulas, 
                this->decision_classes_count, 
                data[i].data[j],
                data[i].attributes_count
            );

            if (i==vote_result) {
                score++;
            }
        }
        all+=data[i].rows_count;
    }

    return score / (float) all;
}

bool RandomClassifier::satisfiableFormulasCountGenerated()
{
    for(int i=0; i<this->decision_classes_count; i++) {
        int formulas_size = this->decision_class_formulas[i].size();

        if (formulas_size<this->formulas_count) {
            return false;
        }
    }
    return true;
}

void RandomClassifier::clearWeakestFormulas(std::list<Formula> & formulas, Data * data, int class_index)
{
    auto formula = formulas.begin();
    while (formula != formulas.end()) {
        if (!this->evaluator->formulaIsEfficient(data, this->decision_classes_count, *formula, class_index)) {
            formulas.erase(formula++);
        } else {
            ++formula;
        }
    }
}

void RandomClassifier::saveFormulasToFile(std::string file_name)
{
    std::ofstream formulas_file(file_name);
    
    for(int i=0; i<this->decision_classes_count; i++) {
        formulas_file << i << '\n';
        for(Formula formula : this->decision_class_formulas[i]) {
            formulas_file << stringifyFormula(formula) << '\n';
        }
    }

    formulas_file.close();
}