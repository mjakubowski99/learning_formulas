#include "types.hpp"
#include <map>

#ifndef formulas_hpp
#define formulas_hpp

bool evaluateFormula(std::map<int, Dataframe> & data, Formula formula, bool vote_for_true);

FormulaScore getScore(Dataframe & data, Formula formula, bool goal);

FormulaScore getScoreForRow(Row row, std::list<Formula>  & formulas, bool goal);

bool isFormulaSatisfied(Row row, Formula formula);

void displayFormula(Formula formula);

void displayLiteral(Literal literal);

#endif