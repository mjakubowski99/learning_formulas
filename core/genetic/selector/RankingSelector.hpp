#include "FormulaSelector.hpp"

class RankingSelector : public FormulaSelector {
    int treshold;
    public:
        RankingSelector(int treshold);
        FormulaWithScoreArray select(FormulaWithScoreArray formulas);
};