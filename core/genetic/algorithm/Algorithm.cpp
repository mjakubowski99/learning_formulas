#include "Algorithm.hpp"
#include "../../utils.hpp"

Algorithm::Algorithm(FormulaGenerator * generator, FormulaEvaluator * evaluator)
{
    this->generator = generator;
    this->evaluator = evaluator;
}

void Algorithm::setData(Data * data, int classes_count)
{
    this->data = data;
    this->classes_count = classes_count;
    this->formulas = new FormulaWithScoreArray[this->classes_count];
}

void Algorithm::setFormulasSizeConstant(bool formulas_size_constant)
{
    
}

void Algorithm::setFormulaParams(int formulas_count, int clauses_count, int literals_count)
{
    this->formulas_count = formulas_count;
    this->clauses_count = clauses_count;
    this->literals_count = literals_count;
}

void Algorithm::setSelectionStrategy(FormulaSelector * selector)
{
    this->selector = selector;
}

void Algorithm::setCrossingStrategy(FormulaCrosser * crosser)
{
    this->crosser = crosser;
}

void Algorithm::setPopulationSize(int population_size)
{
    this->poulation_size = population_size;
}

void Algorithm::setPopulationsCount(int populations_count)
{
    this->populations_count = populations_count;
}

void Algorithm::setMutationsPercent(float mutations_percent)
{
    this->mutations_percent = mutations_percent;
}

FormulaWithScoreArray * Algorithm::run()
{
    for(int i=0; i<this->classes_count; i++) {
        this->formulas[i] = this->attachScore(this->generateInitialPopulation(i), i);

        int p=0;
        while (p<this->populations_count) {
            this->formulas[i] = this->selector->select(this->formulas[i]);

            this->performCrossing(i);
            this->mutate(i);

            p++;
        }
    }

    return this->formulas;
}

std::list<Formula> Algorithm::generateInitialPopulation(int goal)
{
    return this->generator->makeFormulas(
        this->data,
        this->classes_count,
        this->formulas_count * 10,
        this->clauses_count, 
        this->literals_count,
        goal,
        false
    );
}

FormulaWithScoreArray Algorithm::attachScore(std::list<Formula> formulas, int goal)
{
    FormulaWithScoreArray formula_with_scores(formulas.size());

    int i=0;
    for(Formula formula : formulas) {
        FormulaWithScore formula_with_score;
        formula_with_score.formula = formula;
        formula_with_score.score = this->evaluator->numericScore(formula, this->data, this->classes_count, goal);

        formula_with_scores.formulas[i] = formula_with_score;
        i++;
    }

    return formula_with_scores;
}

void Algorithm::performCrossing(int decision_class)
{
    FormulaWithScoreArray formulas = this->formulas[decision_class];
    FormulaWithScoreArray new_formulas(this->poulation_size);

    for(int i=0; i<this->poulation_size; i++) {
        int a = randomInt(0, this->formulas[decision_class].size);
        int b = randomInt(0, this->formulas[decision_class].size);
        while(a==b) {
            b = randomInt(0, this->formulas[decision_class].size);
        }

        new_formulas.formulas[i].formula = this->crosser->cross(formulas.formulas[a].formula, formulas.formulas[b].formula);
        new_formulas.formulas[i].score = this->evaluator->numericScore(new_formulas.formulas[i].formula, this->data, this->classes_count, decision_class);
    }

    this->formulas[decision_class] = new_formulas;
}

void Algorithm::mutate(int decision_class)
{
    FormulaWithScoreArray formulas = this->formulas[decision_class];
    int mutations_count = (int) (this->mutations_percent * formulas.size);

    for(int i=0; i<mutations_count; i++) {
        int random = randomInt(0, formulas.size);
        Formula formula = formulas.formulas[random].formula;

        int random_clause = randomInt(0,formula.size());
        int random_literal = randomInt(0,formula[random_clause].size());

        formulas.formulas[random].formula[random_clause][random_literal].positive = 
            !formulas.formulas[random].formula[random_clause][random_literal].positive;
    }

    this->formulas[decision_class] = formulas;
}

float Algorithm::score(Data * data)
{
    int max_votes = 0;
    int predicted_class = 0;

    int score=0;
    int all=0;

    std::list<Formula> * formulas = new std::list<Formula>[this->classes_count];
    for(int i=0; i<this->classes_count; i++) {
        for(int w=0; w<this->formulas[i].size; w++) {
            formulas[i].push_back(this->formulas[i].formulas[w].formula);
        }

        for(int j=0; j<data[i].rows_count; j++) {
            int vote_result = this->evaluator->voteForRow(
                formulas,
                this->classes_count, 
                data[i],
                j,
                data[i].attributes_count
            );

            if (i==vote_result) {
                score++;
            }
        }
        all+=data[i].rows_count;
    }

    return score / (float) all;
}
