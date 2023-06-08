#include "types.hpp"
#include "utils.hpp"
#include "RandomClassifier.hpp"
#include <iostream>
#include <fstream>
#include <ctime>
#include <sstream>
#include "genetic/algorithm/Algorithm.hpp"
#include "genetic/crosser/OnePointCrosser.hpp"
#include "genetic/selector/RankingSelector.hpp"

int decision_classes_count = 0;

std::string train_file_name = "../data/train.txt";
std::string test_file_name = "../data/test.txt";
int max_cycles_count_param = 20;
int formulas_count_param = 100;
int clauses_count_param = 5;
int literals_count_param = 3;
float positive_responses_percentage = 0.4;
std::string result_dir = "/src/result/";

Data * parseData(std::string file_name)
{
    ifstream file(file_name);
    file >> decision_classes_count;

    Data * data = new Data[decision_classes_count];
    for(int i=0; i<decision_classes_count; i++) {
        int rows_count, attributes_count;
        file >> rows_count >> attributes_count;
        data[i].rows_count = rows_count;
        data[i].attributes_count = attributes_count;

        data[i].init(rows_count);
        for (int j=0; j<rows_count; j++) {
            data[i].data[j] = new bool[attributes_count];
            for (int k=0; k<attributes_count; k++) {
                bool bit;
                file >> bit;
                data[i].insert(j,k,bit);
            }
        }
    }
    file.close();

    return data;
}

void parse_args(int argc, char * argv[]) 
{
    if (argc>=2) {
        std::string train_pom(argv[1]);
        train_file_name = train_pom;
    }
    if (argc>=3) {
        std::string test_pom(argv[2]);
        test_file_name = test_pom;
    }
    if (argc>=4) {
        max_cycles_count_param = std::stoi(argv[3]);
    }
    if (argc>=5) {
        formulas_count_param = std::stoi(argv[4]);
    }
    if (argc>=6) {
        clauses_count_param = std::stoi(argv[5]);
    }
    if (argc>=7) {
        literals_count_param = std::stoi(argv[6]);
    }
    if (argc>=8) {
        positive_responses_percentage = std::stoi(argv[7])/100.0;
    }
    if (argc>=9) {
        std::string pom(argv[9]);
        result_dir = pom;
    }
}

void saveFormulasToFile(FormulaWithScoreArray * formulas, int classes_count, std::string file_name)
{
    std::cout << file_name << std::endl;
    std::ofstream formulas_file(file_name);
    std::set<std::string> formula_strings;
    
    for(int i=0; i<classes_count; i++) {
        formulas_file << i << '\n';

        for(int j=0; j<formulas[i].size; j++) {
            std::string f = stringifyFormula(formulas[i].formulas[j].formula);
            formulas_file << f << '\n';
        }
    }

    formulas_file.close();
}

int main(int argc, char * argv[]) {
    parse_args(argc, argv);
    
    std::cout << "Algorithm started with: " << std::endl;
    std::cout << "Runned for file: " << train_file_name << std::endl;
    std::cout << "Test file: " << test_file_name << std::endl;
    std::cout << "Cycles count: " << max_cycles_count_param << std::endl;
    std::cout << "Formulas count for class: " << formulas_count_param << std::endl;
    std::cout << "Clauses count in formula: " << clauses_count_param << std::endl;
    std::cout << "Literals count in formula: " << literals_count_param << std::endl;
    std::cout << "Positive responses percentage for decision class: " << positive_responses_percentage << std::endl;

    Data * train_data = parseData(train_file_name);

    std::cout << "Running algorithm..." << std::endl;

    FormulaGenerator * generator = new FormulaGenerator;
    FormulaEvaluator * evaluator = new FormulaEvaluator(positive_responses_percentage);

    Algorithm algorithm(generator, evaluator);
    FormulaCrosser * crosser = new OnePointCrosser;
    FormulaSelector * selector = new RankingSelector(20);

    algorithm.setData(train_data, decision_classes_count);
    algorithm.setCrossingStrategy(crosser);
    algorithm.setSelectionStrategy(selector);
    algorithm.setFormulaParams(formulas_count_param, clauses_count_param, literals_count_param);
    algorithm.setPopulationsCount(200);
    algorithm.setPopulationSize(100);
    algorithm.setMutationsPercent(0.05);

    FormulaWithScoreArray * formula_with_score_array = algorithm.run();

    Data * test_data = parseData(test_file_name);
    saveFormulasToFile(formula_with_score_array, decision_classes_count, result_dir+"result.txt");

    std::cout << algorithm.score(test_data) << std::endl;
    /**
    std::cout << "Running algorithm..." << std::endl;

    FormulaGenerator * generator = new FormulaGenerator;
    FormulaEvaluator * evaluator = new FormulaEvaluator(positive_responses_percentage);

    Algorithm algorithm(generator, evaluator);
    FormulaCrosser * crosser = new OnePointCrosser;
    FormulaSelector * selector = new RankingSelector(20);

    algorithm.setData(train_data, decision_classes_count);
    algorithm.setCrossingStrategy(crosser);
    algorithm.setSelectionStrategy(selector);
    algorithm.setFormulaParams(formulas_count_param, clauses_count_param, literals_count_param);
    algorithm.setPopulationsCount(1000);
    algorithm.setPopulationSize(30);

    FormulaWithScoreArray * formula_with_score_array = algorithm.run();

    Data * test_data = parseData(test_file_name);
    saveFormulasToFile(formula_with_score_array, decision_classes_count, result_dir+"result.txt");

    std::cout << algorithm.score(test_data) << std::endl;

    /**
    RandomClassifier clf(
        decision_classes_count, 
        max_cycles_count_param, 
        formulas_count_param, 
        clauses_count_param, 
        literals_count_param,
        positive_responses_percentage
    );
    clf.fit(train_data);

    delete train_data;

    Data * test_data = parseData(test_file_name);
    std::cout << clf.score(test_data) << std::endl;

    std::time_t ms = std::time(nullptr);

    std::stringstream stream;
    stream << result_dir << ms;

    clf.saveFormulasToFile(result_dir+"result.txt");
    **/
    return 0;
}