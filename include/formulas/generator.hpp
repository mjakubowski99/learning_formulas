#include "types.hpp"
#include <set>
#include <vector>
#include <list>
#include <map>

#ifndef generator_h
#define generator_h

void generateFormulas(FormulaVote & formula_vote, std::map<int, Dataframe> & data, int formulas_count, int clauses_count, int literals_count, int goal);

void generatePositiveFormulas(FormulaVote & formula_vote, Dataframe dataframe, int formulas_count, int clauses_count, int literals_count);

void generateNegativeFormulas(FormulaVote &  formula_vote, Dataframe dataframe, int formulas_count, int clauses_count, int literals_count);

int randomIndex(int min, int max, std::set<int> & drawn);

#endif

