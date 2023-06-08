#include "RankingSelector.hpp"
#include <algorithm>

RankingSelector::RankingSelector(int treshold)
{
    this->treshold = treshold;
}

FormulaWithScoreArray RankingSelector::select(FormulaWithScoreArray formulas)
{
    sort(formulas.formulas, formulas.formulas+formulas.size, [](FormulaWithScore & a, FormulaWithScore & b) {return a.score > b.score;});

    FormulaWithScoreArray result(this->treshold);

    for(int i=0; i<treshold; i++) {
        result.formulas[i] = formulas.formulas[i];
    }
    
    return result;
}