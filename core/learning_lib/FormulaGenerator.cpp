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
    int min_clauses_count, 
    int max_clauses_count,
    int min_literals_count,
    int max_literals_count, 
    int goal
)
{
    std::list<Formula> positive_formulas;
    std::list<Formula> negative_formulas;

    int positive_count = (formulas_count / 2);
    int negative_count = (formulas_count / 2);

    this->makePositiveFormulas(
        positive_formulas, 
        data[goal], 
        positive_count, 
        min_clauses_count, 
        max_clauses_count, 
        min_literals_count, 
        max_literals_count
    );
    this->makeNegativeFormulas(
        negative_formulas, 
        data, 
        goal, 
        classes_count, 
        negative_count, 
        min_clauses_count, 
        max_clauses_count, 
        min_literals_count, 
        max_literals_count
    );

    for(Formula formula : negative_formulas) {
        positive_formulas.push_back(formula);
    }
    
    return positive_formulas;
}

void FormulaGenerator::makePositiveFormulas(
    std::list<Formula> & positive_formulas, 
    Data data,
    int formulas_count, 
    int min_clauses_count, 
    int max_cluases_count,
    int min_literals_count,
    int max_literals_count
)
{
    int rows = data.rows_count;
    int cols = data.attributes_count;
    

    for(int i=0; i<formulas_count; i++) {
        Formula formula;

        int final_clauses_count = min_clauses_count==max_cluases_count ? max_cluases_count : randomInt(min_clauses_count,max_cluases_count);
        for(int j=0; j<final_clauses_count; j++) {
            std::set<int> drawn_rows;
            std::set<int> drawn_cols;

            Clause clause;
            int final_literals_count = min_literals_count == max_literals_count ? min_literals_count : randomInt(min_literals_count,max_literals_count);
            for(int k=0; k<final_literals_count; k++) {
                int random_row = this->randomIndex(0, rows, drawn_rows);
                int random_col = this->randomIndex(0, cols, drawn_cols);

                Literal literal(random_col, data.get(random_row,random_col));
                clause.push_back(literal);
            }
            formula.push_back(clause);
        }
        positive_formulas.push_back(formula);
    }
}

void FormulaGenerator::makeNegativeFormulas(
    std::list<Formula> & negative_formulas, 
    Data * data,
    int goal,
    int classes_count,
    int formulas_count, 
    int min_clauses_count, 
    int max_cluases_count,
    int min_literals_count,
    int max_literals_count
)
{
    int d_class = 0;
    for(int i=0; i<formulas_count; i++) {
        Formula formula;

        while (d_class==goal) {
            d_class++;
            if (d_class>=classes_count) {
                d_class=0;
            }
        }

        Data decision_class_data = data[d_class];

        int final_clauses_count = min_clauses_count==max_cluases_count ? max_cluases_count : randomInt(min_clauses_count,max_cluases_count);
        for(int j=0; j<final_clauses_count; j++) {

            int rows = data[d_class].rows_count;
            int cols = data[d_class].attributes_count;

            std::set<int> drawn_cols;
        
            int random_row = randomInt(0,classes_count);

            Clause clause;
            int final_literals_count = min_literals_count == max_literals_count ? min_literals_count : randomInt(min_literals_count,max_literals_count);
            for(int k=0; k<final_literals_count; k++) {
                int random_col = this->randomIndex(0, cols, drawn_cols);

                Literal literal(random_col, !decision_class_data.get(random_row, random_col));
                clause.push_back(literal);
            }
            formula.push_back(clause);
        }
        negative_formulas.push_back(formula);

        d_class++;
        if (d_class>=classes_count) {
            d_class=0;
        }
    }
}

int FormulaGenerator::randomIndex(int min, int max, std::set<int> & drawn)
{
    int random = randomInt(min,max);

    int i = 0;
    int tries = 100000;

    while(drawn.find(random) != drawn.end() && i<tries) {
        random = randomInt(min,max);
        i++;
    }

    drawn.insert(random);
    return random;
}