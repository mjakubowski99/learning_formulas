#pragma once

#include "types.hpp"
#include "FormulaGenerator.hpp"
#include "FormulaEvaluator.hpp"

class Algorithm {
    Data * data;
    int populations_count;
    int final_population_size;
    int poulation_size;
    float new_formulas_percentage;
    int min_clauses_count;
    int max_clauses_count;
    int min_literals_count;
    int max_literals_count;
    int classes_count;
    int keep_best;
    std::string formula_evaluation_type;
    FormulaGenerator * generator;
    FormulaEvaluator * evaluator;

    FormulaWithScoreArray * formulas;

    public:
        Algorithm(FormulaGenerator * generator, FormulaEvaluator * evaluator);

        void setData(Data * data, int classes_count);

        void setFormulaParams(
            int min_clauses_count, 
            int max_clauses_count, 
            int min_literals_count, 
            int max_literals_count
        );

        void setFormulaEvaluationType(std::string formula_evaluation_type);

        void setPopulationSize(int population_size);

        void setPopulationsCount(int populations_count);

        void setNewFormulasPercentage(float new_formulas_percentage);

        void setFinalPopulationSize(int final_population_size);

        FormulaWithScoreArray * run();

        float score(Data * data);
    private:
        std::list<Formula> generateInitialPopulation(int goal);

        FormulaWithScoreArray attachScore(std::list<Formula> formulas, int goal);

        void performCrossing(int decision_class);

        void improveFormulas(int decision_class);
};