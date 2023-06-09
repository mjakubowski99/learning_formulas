#pragma once

#include "types.hpp"
#include "FormulaGenerator.hpp"
#include "FormulaEvaluator.hpp"
#include <vector>
#include <list>
#include <string>

class RandomClassifier
{
    FormulaGenerator * generator;

    FormulaEvaluator * evaluator;

    std::list<Formula> * decision_class_formulas;

    int decision_classes_count;

    int cycles_count;
    
    int formulas_count;

    int min_clauses_count;

    int max_clauses_count;

    int min_literals_count;

    int max_literals_count;

    public:
        RandomClassifier(
            int decision_classes_count, 
            int cycles_count, 
            int formulas_count, 
            int min_clauses_count,
            int max_clauses_count, 
            int min_literals_count,
            int max_literals_count,
            float positive_responses_treshold
        );

        void fit(Data * data);

        float score(Data * data);

        void saveFormulasToFile(std::string file_name);
    private:
        bool satisfiableFormulasCountGenerated();

        void clearWeakestFormulas(std::list<Formula> & formulas, Data * data, int class_index);
};