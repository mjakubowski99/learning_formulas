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
    int goal,
    bool constant_size
)
{
    std::list<Formula> positive_formulas;
    std::list<Formula> negative_formulas;

    int positive_count = (formulas_count / 2);
    int negative_count = (formulas_count / 2);

    this->makePositiveFormulas(positive_formulas, data[goal], positive_count, clauses_count, literals_count, constant_size);
    this->makeNegativeFormulas(negative_formulas, data, goal, classes_count, negative_count, clauses_count, literals_count, constant_size);

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
    int literals_count,
    bool constant_size=true
)
{
    int rows = data.rows_count;
    int cols = data.attributes_count;
    
    for(int i=0; i<formulas_count; i++) {
        Formula formula;

        int final_clauses_count = constant_size ? clauses_count : randomInt(1,clauses_count);
        for(int j=0; j<final_clauses_count; j++) {
            std::set<int> drawn_rows;
            std::set<int> drawn_cols;

            Clause clause;
            int final_literals_count = constant_size ? literals_count : randomInt(1,literals_count);
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
    int clauses_count, 
    int literals_count,
    bool constant_size=true
)
{
    for(int i=0; i<formulas_count; i++) {
        Formula formula;

        int final_clauses_count = constant_size ? clauses_count : randomInt(2,clauses_count);
        for(int j=0; j<final_clauses_count; j++) {
            int d_class = randomInt(0,classes_count);
            while (d_class == goal)
            {
                d_class = randomInt(0,classes_count);
            }

            int rows = data[d_class].rows_count;
            int cols = data[d_class].attributes_count;

            std::set<int> drawn_cols;
        
            int random_row = randomInt(0,classes_count);

            Clause clause;
            int final_literals_count = constant_size ? literals_count : randomInt(1,literals_count);
            for(int k=0; k<final_literals_count; k++) {
                int random_col = this->randomIndex(0, cols, drawn_cols);

                Literal literal(random_col, !data[d_class].get(random_row, random_col));
                clause.push_back(literal);
            }
            formula.push_back(clause);
        }
        negative_formulas.push_back(formula);
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