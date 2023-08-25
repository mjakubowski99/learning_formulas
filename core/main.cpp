#include <iostream>
#include <fstream>
#include <ctime>
#include <sstream>
#include <filesystem>

#include <utils.hpp>
#include <types.hpp>
#include <FormulaGenerator.hpp>
#include <Algorithm.hpp>

int decision_classes_count = 0;

std::string train_file_name = "../data/train.txt";
std::string test_file_name = "../data/test.txt";
std::string algorithm = "EVOLUTION";
std::string formula_evaluation_type = "F_MEASURE";

int formulas_count_param = 100;
int min_clauses_count = 5;
int max_clauses_count = 5;
int min_literals_count = 5;
int max_literals_count = 5;
std::string result_dir = "../result/";
int populations_count = 100;
int population_size = 300;
int final_population_size = 100;
float new_formulas_percentage = 0.1;
float crossing_percentage = 0.3;

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
        std::string pom(argv[3]);
        result_dir = pom;
    }
    if (argc>=5) {
        std::string test_pom(argv[4]);
        algorithm = test_pom;
    }
    if (argc>=6) {
        min_clauses_count = std::stoi(argv[5]);
    }
    if (argc>=7) {
        max_clauses_count = std::stoi(argv[6]);
    }
    if (argc>=8) {
        min_literals_count = std::stoi(argv[7]);
    }
    if (argc>=9) {
        max_literals_count = std::stoi(argv[8]);
    }

    if (algorithm == "EVOLUTION") {
        if (argc>=10) {
            populations_count = std::stoi(argv[9]);
        }
        if (argc>=11) {
            population_size = std::stoi(argv[10]);
        }
        if (argc>=12) {
            final_population_size = std::stoi(argv[11]);
        }
        if (argc>=13) {
            new_formulas_percentage = std::stof(argv[12]);
        }
        if (argc>=14) {
            std::string test_pom(argv[13]);
            formula_evaluation_type = test_pom;
            std::cout << "Evaluation type" << formula_evaluation_type << std::endl;
        }
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

void saveReport(float result)
{
    std::ifstream infile(result_dir+"report.csv");
    bool file_exists = infile.good();
    infile.close();

    std::ofstream report_file(result_dir+"report.csv", std::ios_base::app);

    if (!file_exists) {
        report_file << "populations_count,populaton_size,min_clauses_count,max_clauses_count,min_literals_count,max_literals_count,";
        report_file << "final_population_size,new_formulas_percentage,crossing_percentage,result\n";
    }

    report_file << populations_count << ",";
    report_file << population_size << ",";
    report_file << min_clauses_count << ",";
    report_file << max_clauses_count << ",";
    report_file << min_literals_count << ",";
    report_file << max_literals_count << ",";
    report_file << final_population_size << ",";
    report_file << (int) (population_size*new_formulas_percentage) << ",";
    report_file << (int) (population_size*crossing_percentage) << ",";
    report_file << result << "\n";

    report_file.close();
}

void saveFormulasWithScoreToFile(FormulaWithScoreArray * formulas, int classes_count, std::string file_name)
{
    std::cout << file_name << std::endl;
    std::ofstream formulas_file(file_name);
    std::set<std::string> formula_strings;
    
    for(int i=0; i<classes_count; i++) {
        formulas_file << i << '\n';

        for(int j=0; j<formulas[i].size; j++) {
            std::string f = stringifyFormula(formulas[i].formulas[j].formula);
            formulas_file << f << " - " << formulas[i].formulas[j].score << '\n';
        }
    }

    formulas_file.close();
}

int main(int argc, char * argv[]) {
    parse_args(argc, argv);

    Data * train_data = parseData(train_file_name);
    Data * test_data = parseData(test_file_name);

    std::cout << "Started evolation" << std::endl;
    std::cout << "Algorithm started with: " << std::endl;
    std::cout << "Runned for file: " << train_file_name << std::endl;
    std::cout << "Test file: " << test_file_name << std::endl;
    std::cout << "Populations count: " << populations_count << std::endl;
    std::cout << "Population size: " << population_size << std::endl;
    std::cout << "New formulas percentage: " << new_formulas_percentage << std::endl;
    std::cout << "Crossing percentage: " << crossing_percentage << std::endl;
    std::cout << "Min clauses count in formula: " << min_clauses_count << std::endl;
    std::cout << "Max clauses count in formula: " << max_clauses_count << std::endl;
    std::cout << "Min literals count in formula: " << min_literals_count << std::endl;
    std::cout << "Max literals count in formula: " << max_literals_count << std::endl;
    std::cout << "Final population size: " << final_population_size << std::endl;
    std::cout << "Evaluation type: " << formula_evaluation_type << std::endl;

    FormulaGenerator * generator = new FormulaGenerator;
    FormulaEvaluator * evaluator = new FormulaEvaluator(0.4);

    Algorithm algorithm(generator, evaluator);

    algorithm.setData(train_data, decision_classes_count);
    algorithm.setFormulaParams(
        min_clauses_count, 
        max_clauses_count, 
        min_literals_count, 
        max_literals_count
    );
    algorithm.setFormulaEvaluationType(formula_evaluation_type);
    algorithm.setPopulationsCount(populations_count);
    algorithm.setPopulationSize(population_size);
    algorithm.setNewFormulasPercentage(new_formulas_percentage);
    algorithm.setFinalPopulationSize(final_population_size);

    FormulaWithScoreArray * formula_with_score_array = algorithm.run();

    saveFormulasWithScoreToFile(formula_with_score_array, decision_classes_count, result_dir+"result.txt");
    float score = algorithm.score(train_data);
    saveReport(score);
    std::cout << "Score: " << score << std::endl;

    return 0;
}