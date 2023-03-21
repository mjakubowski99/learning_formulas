#include "types.hpp"
#include "FormulaClassifier.hpp"
#include "FormulaGenerator.hpp"
#include "FormulaEvaluator.hpp"
#include <vector>

class RandomClassifier : public FormulaClassifier 
{
    FormulaGenerator generator;

    FormulaEvaluator evaluator;

    DecisionClass * decision_classes;

    int decision_classes_count;

    int cycles_count;
    
    int formulas_count;

    int clauses_count;

    int literals_count;

    public:
        RandomClassifier(int cycles_count, int formulas_count, int clauses_count, int literals_count);

        void fit(Data * data, int classes_count);

        void score(Data * data, int classes_count);
    private:
        bool satisfiableFormulasCountGenerated(Data * data, int classes_count)

        void clearWeakestFormualas(Data * data, int classes_count);
}