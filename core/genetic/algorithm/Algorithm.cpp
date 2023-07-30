#include "Algorithm.hpp"
#include "../../utils.hpp"

Algorithm::Algorithm(FormulaGenerator * generator, FormulaEvaluator * evaluator)
{
    this->generator = generator;
    this->evaluator = evaluator;
}

void Algorithm::setData(Data * data, Data * test_data, int classes_count)
{
    this->data = data;
    this->test_data = test_data;
    this->classes_count = classes_count;
    this->formulas = new FormulaWithScoreArray[this->classes_count];
}

void Algorithm::setFormulaParams(
    int min_clauses_count, 
    int max_clauses_count, 
    int min_literals_count, 
    int max_literals_count,
    int keep_best
)
{
    this->final_population_size = final_population_size;
    this->min_clauses_count = min_clauses_count;
    this->max_clauses_count = max_clauses_count;
    this->min_literals_count = min_literals_count;
    this->max_literals_count = max_literals_count;
    this->keep_best = keep_best;
}

void Algorithm::setSelectionStrategy(FormulaSelector * selector)
{
    this->selector = selector;
}

void Algorithm::setCrossingStrategy(FormulaCrosser * crosser)
{
    this->crosser = crosser;
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
            //this->formulas[i] = this->selector->select(this->formulas[i]);
            this->formulas[i].sortByScore();

            //this->performCrossing(i);
            this->mutate(i);

            std::cout << "Populacja: " << p << std::endl;
            p++;
        }

        this->formulas[i].sortByScore();
        this->formulas[i].size = this->final_population_size;
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

    if (this->keep_best > this->poulation_size) {
        this->keep_best = this->poulation_size;
    }

    for(int i=0; i<this->keep_best; i++) {
        new_formulas.formulas[i] = this->formulas[decision_class].formulas[i];
    }
    for(int i=this->keep_best; i<this->poulation_size; i++) {
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

        int formula_mutations_count = randomInt(0,formula.size());

        std::list<Formula> generated_formulas;

        this->generator->makePositiveFormulas(
            generated_formulas,
            this->data[decision_class],
            (int) (formula_mutations_count/2),
            this->min_clauses_count,
            this->max_clauses_count,
            this->min_literals_count,
            this->max_literals_count
        );
        this->generator->makeNegativeFormulas(
            generated_formulas,
            this->data,
            decision_class,
            this->classes_count,
            (int) (formula_mutations_count/2),
            this->min_clauses_count,
            this->max_clauses_count,
            this->min_literals_count,
            this->max_literals_count
        );

        FormulaWithScoreArray gen_formulas = this->attachScore(generated_formulas, decision_class);
        gen_formulas.sortByScore();

        int size = formulas.size;
        
        int j=0;
        for(int i=size-1; i>=size-gen_formulas.size; i--) {
            if (gen_formulas.formulas[j].score > formulas.formulas[j].score) {
                formulas.formulas[i] = gen_formulas.formulas[j];
            }
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
