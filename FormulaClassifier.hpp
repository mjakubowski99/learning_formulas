#include "types.hpp"
#include <map>

class FormulaGenerator {
    public:
        void makeFormulas(FormulaVote & formula_vote, Data data, FormulaParameters parameters, bool goal);

        void makePositiveFormulas(FormulaVote & formula_vote, Data data, FormulaParameters parameters);

        void makeNegativeFormulas(FormulaVote & formula_vote, Data data, FormulaParameters parameters);

        int randomIndex(int min, int max, set<int> & drawn);
}