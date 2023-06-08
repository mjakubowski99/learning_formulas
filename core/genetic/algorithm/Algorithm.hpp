#pragma once

#include "../../types.hpp"
#include "../../FormulaGenerator.hpp"
#include "../../FormulaEvaluator.hpp"
#include "../crosser/FormulaCrosser.hpp"
#include "../selector/FormulaSelector.hpp"

class Algorithm {
    Data * data;
    int populations_count;
    int poulation_size;
    float mutations_percent;
    int formulas_count;
    int clauses_count;
    int literals_count;
    int classes_count;
    FormulaGenerator * generator;
    FormulaEvaluator * evaluator;
    FormulaSelector * selector;
    FormulaCrosser * crosser;

    FormulaWithScoreArray * formulas;

    public:
        Algorithm(FormulaGenerator * generator, FormulaEvaluator * evaluator);

        void setData(Data * data, int classes_count);

        void setFormulasSizeConstant(bool formulas_size_constant);

        void setFormulaParams(int formulas_count, int clauses_count, int literals_count);

        void setSelectionStrategy(FormulaSelector * selector);

        void setCrossingStrategy(FormulaCrosser * crosser);

        void setPopulationSize(int population_size);

        void setPopulationsCount(int populations_count);

        void setMutationsPercent(float mutations_percent);

        FormulaWithScoreArray * run();

        float score(Data * data);
    private:
        std::list<Formula> generateInitialPopulation(int goal);

        FormulaWithScoreArray attachScore(std::list<Formula> formulas, int goal);

        void performCrossing(int decision_class);

        void mutate(int decision_class);
};