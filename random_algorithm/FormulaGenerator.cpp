#include <cstdlib>
#include <ctime>
#include "FormulaGenerator.hpp"
#include "types.hpp"
#include <iostream>
#include <list> 
#include "utils.hpp"

std::list<Formula> FormulaGenerator::makeFormulas(
    Data * data, 
    int classes_count, 
    int formulas_count, 
    int clauses_count, 
    int literals_count, 
    int goal
)
{
    std::list<Formula> positive_formulas;
    std::list<Formula> negative_formulas;

    int positive_count = (formulas_count / 2);
    this->makePositiveFormulas(positive_formulas, data[goal], positive_count, clauses_count, literals_count);
    int negative_count = (formulas_count/2) / (classes_count-1);

    for(int i=0; i<classes_count; i++) {
        if (i != goal) {
            this->makeNegativeFormulas(negative_formulas, data[i], negative_count, clauses_count, literals_count);
        }
    }

    if (negative_formulas.size() < positive_count) {
        int expected_negative_count = positive_count - negative_formulas.size();
        for(int i=0; i<classes_count; i++) {
            if (i != goal) {
                this->makeNegativeFormulas(negative_formulas, data[i], negative_count, clauses_count, literals_count);
                break;
            }
        }
    }

    for(Formula formula : negative_formulas) {
        positive_formulas.push_back(formula);
    }
    
    return positive_formulas;
}

void FormulaGenerator::makePositiveFormulas(
    std::list<Formula> & positive_formulas, 
    Data data,
    int formulas_count, 
    int clauses_count, 
    int literals_count
)
{
    srand((unsigned) time(NULL));
    int rows = data.rows_count;
    int cols = data.attributes_count;
    
    for(int i=0; i<formulas_count; i++) {
        Formula formula;

        for(int j=0; j<clauses_count; j++) {
            std::set<int> drawn_rows;
            std::set<int> drawn_cols;

            Clause clause;
            for(int k=0; k<literals_count; k++) {
                int random_row = this->randomIndex(0, rows, drawn_rows);
                int random_col = this->randomIndex(0, cols, drawn_cols);

                Literal literal(random_col, data.data[random_row][random_col]);
                clause.push_back(literal);
            }
            formula.push_back(clause);
        }
        positive_formulas.push_back(formula);
    }
}

void FormulaGenerator::makeNegativeFormulas(
    std::list<Formula> & negative_formulas, 
    Data data,
    int formulas_count, 
    int clauses_count, 
    int literals_count
)
{
    srand((unsigned) time(NULL));
    int rows = data.rows_count;
    int cols = data.attributes_count;
    
    for(int i=0; i<formulas_count; i++) {
        Formula formula;

        for(int j=0; j<clauses_count; j++) {
            std::set<int> drawn_cols;
            int random_row = (rand() % rows);

            Clause clause;
            for(int k=0; k<literals_count; k++) {
                int random_col = this->randomIndex(0, cols, drawn_cols);

                Literal literal(random_col, !data.data[random_row][random_col]);
                clause.push_back(literal);
            }
            formula.push_back(clause);
        }
        negative_formulas.push_back(formula);
    }
}

int FormulaGenerator::randomIndex(int min, int max, std::set<int> & drawn)
{
    int random = (rand() % max) + min;

    int i = 0;
    int tries = 100000;

    while(drawn.find(random) != drawn.end() && i<tries) {
        random = (rand() % max) + min;
        i++;
    }

    drawn.insert(random);
    return random;
}