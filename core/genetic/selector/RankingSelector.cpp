#include "RankingSelector.hpp"

RankingSelector::RankingSelector(int treshold)
{
    this->treshold = treshold;
}

FormulaWithScoreArray RankingSelector::select(FormulaWithScoreArray formulas)
{
    formulas.sortByScore();
    FormulaWithScoreArray result(this->treshold);

    for(int i=0; i<treshold; i++) {
        result.formulas[i] = formulas.formulas[i];
    }
    
    return result;
}