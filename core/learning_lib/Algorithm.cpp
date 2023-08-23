#include "Algorithm.hpp"
#include "utils.hpp"

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

void Algorithm::setFormulaParams(
    int min_clauses_count, 
    int max_clauses_count, 
    int min_literals_count, 
    int max_literals_count
)
{
    this->final_population_size = final_population_size;
    this->min_clauses_count = min_clauses_count;
    this->max_clauses_count = max_clauses_count;
    this->min_literals_count = min_literals_count;
    this->max_literals_count = max_literals_count;
}

void Algorithm::setFinalPopulationSize(int final_population_size)
{
    this->final_population_size = final_population_size;
}

void Algorithm::setPopulationSize(int population_size)
{
    this->poulation_size = population_size;
}

void Algorithm::setPopulationsCount(int populations_count)
{
    this->populations_count = populations_count;
}

void Algorithm::setNewFormulasPercentage(float new_formulas_percentage)
{
    this->new_formulas_percentage = new_formulas_percentage;
}

FormulaWithScoreArray * Algorithm::run()
{
    for(int i=0; i<this->classes_count; i++) {
        this->formulas[i] = this->attachScore(this->generateInitialPopulation(i), i);

        int p=0;
        while (p<this->populations_count) {
            this->formulas[i].sortByScore();
            
            this->improveFormulas(i);
            std::cout << "Decision class: " << i << "avg score: " << this->formulas[i].avgScore() << std::endl;
            std::cout << "Iteracja: " << p << std::endl;
            p++;
        }

        this->formulas[i].sortByScore();

        if (this->final_population_size<=this->formulas[i].size) {
            this->formulas[i].size = this->final_population_size;
        }
    }

    return this->formulas;
}

std::list<Formula> Algorithm::generateInitialPopulation(int goal)
{
    return this->generator->makeFormulas(
        this->data,
        this->classes_count,
        this->poulation_size,
        this->min_clauses_count,
        this->max_clauses_count,
        this->min_literals_count,
        this->max_literals_count,
        goal
    );
}

FormulaWithScoreArray Algorithm::attachScore(std::list<Formula> formulas, int goal)
{
    FormulaWithScoreArray formula_with_scores(formulas.size());
    int i=0;
    for(Formula formula : formulas) {
        FormulaWithScore formula_with_score;
        formula_with_score.formula = formula;
        formula_with_score.score = this->evaluator->fMeasureScore(formula, this->data, this->classes_count, goal);
        formula_with_scores.formulas[i] = formula_with_score;
        i++;
    }

    return formula_with_scores;
}

void Algorithm::improveFormulas(int decision_class)
{
    FormulaWithScoreArray formulas = this->formulas[decision_class];
    int new_formulas_count = (int) (this->new_formulas_percentage * formulas.size);

    int formulas_size = this->new_formulas_percentage * this->poulation_size;

    std::list<Formula> generated_formulas = this->generator->makeFormulas(
        this->data,
        this->classes_count,
        formulas_size,
        this->min_clauses_count,
        this->max_clauses_count,
        this->min_literals_count,
        this->max_literals_count,
        decision_class
    );

    FormulaWithScoreArray gen_formulas = this->attachScore(generated_formulas, decision_class);
    gen_formulas.sortByScore();

    int j=0;
    for(int i=0; i<formulas.size && j<gen_formulas.size; i++) {
        if (gen_formulas.formulas[j].score > formulas.formulas[i].score) {
            FormulaWithScore copy = formulas.formulas[i];
            formulas.formulas[formulas.size-1-j] = copy;
            formulas.formulas[i] = gen_formulas.formulas[j];
            j++;
        }

    }
    formulas.sortByScore();

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
    }

    for(int i=0; i<this->classes_count; i++) {
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
