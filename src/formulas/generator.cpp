#include "formulas/generator.hpp"
#include "formulas/formulas.hpp"
#include <cstdlib>
#include <ctime>
#include <iostream>
#include <vector>
#include <map>
using namespace std;

void generateFormulas(FormulaVote & formula_vote, map<int, Dataframe> & data, int formulas_count, int clauses_count, int literals_count, int goal)
{
    int negative = goal == 1 ? 0 : 1;

    generatePositiveFormulas(formula_vote, data[goal], (int) (formulas_count/2), clauses_count, literals_count);
    generateNegativeFormulas(formula_vote, data[negative], (int) (formulas_count/2), clauses_count, literals_count);
}

void generatePositiveFormulas(FormulaVote & formula_vote, Dataframe dataframe, int formulas_count, int clauses_count, int literals_count)
{

    int rows = dataframe.size();
    int cols = dataframe[0].size();

    srand((unsigned) time(NULL));
    
    for(int i=0; i<formulas_count; i++) {
        Formula formula;

        for(int j=0; j<clauses_count; j++) {
            std::set<int> drawn_rows;
            std::set<int> drawn_cols;

            Clause clause;
            for(int k=0; k<literals_count; k++) {
                int random_row = randomIndex(0, rows, drawn_rows);
                int random_col = randomIndex(0, cols, drawn_cols);

                Literal literal(random_col, dataframe[random_row][random_col]);
                clause.push_back(literal);
            }
            formula.push_back(clause);
        }
        formula_vote.positive.push_back(formula);
    }
}

void generateNegativeFormulas(FormulaVote & formula_vote, Dataframe dataframe, int formulas_count, int clauses_count, int literals_count)
{
    int rows = dataframe.size();
    int cols = dataframe[0].size();
    srand((unsigned) time(NULL));
    
    for(int i=0; i<formulas_count; i++) {
        Formula formula;

        for(int j=0; j<clauses_count; j++) {
            std::set<int> drawn_cols;
            int random_row = (rand() % rows);

            Clause clause;
            for(int k=0; k<literals_count; k++) {
                int random_col = randomIndex(0, cols, drawn_cols);

                Literal literal(random_col, !dataframe[random_row][random_col]);
                clause.push_back(literal);
            }
            formula.push_back(clause);
        }
        formula_vote.negative.push_back(formula);
    }
}

int randomIndex(int min, int max, set<int> & drawn)
{
    int random = (rand() % max) + min;

    int i = 0;
    int tries = 10000;

    while(drawn.find(random) != drawn.end() && i<tries) {
        random = (rand() % max) + min;
        i++;
    }

    drawn.insert(random);
    return random;
}