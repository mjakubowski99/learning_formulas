#pragma once

#include "../../types.hpp"

class FormulaSelector {
    public:
        virtual FormulaWithScoreArray select(FormulaWithScoreArray formulas) = 0;
};