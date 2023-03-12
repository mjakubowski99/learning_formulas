#include "classifier/classifier.hpp"
#include "formulas/generator.hpp"
#include "formulas/formulas.hpp"
#include <vector>
#include <iostream>

Classifier::Classifier(int cycles_limit, int expected_formulas_number, int expected_clauses_count, int expected_literals_count)
{
    this->cycles_limit = cycles_limit;
    this->expected_formulas_number = expected_formulas_number;
    this->expetected_clauses_count = expected_clauses_count;
    this->expected_literals_count = expected_literals_count;
}

void Classifier::fit(std::map<int, Dataframe> data)
{
    int i = 0;

    while(i<this->cycles_limit) {
        std::cout << "Cycle number: " << i << std::endl;

        int expected_positive_count = this->expected_formulas_number - this->positive_formulas.positive.size() - this->positive_formulas.negative.size();
        int expected_negative_count = this->expected_formulas_number - this->negative_formulas.positive.size() - this->negative_formulas.negative.size();

        generateFormulas(
            this->positive_formulas, 
            data, 
            this->expected_formulas_number,
            this->expetected_clauses_count,
            this->expected_literals_count,
            1
        );

        generateFormulas(
            this->negative_formulas, 
            data, 
            this->expected_formulas_number,
            this->expetected_clauses_count,
            this->expected_literals_count,
            0
        );

        auto it = this->positive_formulas.positive.begin();
        while (it != this->positive_formulas.positive.end()) {
            if (!evaluateFormula(data, *it, true)) {
                this->positive_formulas.positive.erase(it++);
            }
            else {
                ++it;
            }
        }

        it = this->positive_formulas.negative.begin();
        while (it != this->positive_formulas.negative.end()) {
            if (!evaluateFormula(data, *it, false)) {
                this->positive_formulas.negative.erase(it++);
            }
            else {
                ++it;
            }
        }

        it = this->negative_formulas.positive.begin();
        while (it != this->negative_formulas.positive.end()) {
            if (!evaluateFormula(data, *it, true)) {
                this->negative_formulas.positive.erase(it++);
            }
            else {
                ++it;
            }
        }

        it = this->negative_formulas.negative.begin();
        while (it != this->negative_formulas.negative.end()) {
            if (!evaluateFormula(data, *it, false)) {
                this->negative_formulas.negative.erase(it++);
            }
            else {
                ++it;
            }
        }

        std::cout << "Generated formulas number: " << this->positive_formulas.positive.size() << std::endl;

        i++;

        if (this->positive_formulas.positive.size() > this->expected_formulas_number && this->negative_formulas.positive.size() > this->expected_formulas_number) {
            break;
        }
    }
}

float Classifier::score(std::map<int, Dataframe> data)
{
    int total_frame_size = data[0].size() + data[1].size();
    int total_score = 0;

    for(Row row : data[0]) {
        FormulaScore positive_score = getScoreForRow(row, this->positive_formulas.positive, true);
        FormulaScore negative_score = getScoreForRow(row, this->positive_formulas.negative, false);

        int positive_count = positive_score.true_positives + negative_score.true_negatives;

        positive_score = getScoreForRow(row, this->negative_formulas.positive, true);
        negative_score = getScoreForRow(row, this->negative_formulas.negative, false);

        int negative_count = positive_score.true_positives + negative_score.true_negatives;

        bool is_positive = positive_count > negative_count;
        if (!is_positive) {
            total_score++;
        }
    }

    for(Row row : data[1]) {
        FormulaScore positive_score = getScoreForRow(row, this->positive_formulas.positive, true);
        FormulaScore negative_score = getScoreForRow(row, this->positive_formulas.negative, false);

        int positive_count = positive_score.true_positives + negative_score.true_negatives;

        positive_score = getScoreForRow(row, this->negative_formulas.positive, true);
        negative_score = getScoreForRow(row, this->negative_formulas.negative, false);

        int negative_count = positive_score.true_positives + negative_score.true_negatives;

        bool is_positive = positive_count > negative_count;
        if (is_positive) {
            total_score++;
        }
    }

    return total_score / (float) total_frame_size;
}