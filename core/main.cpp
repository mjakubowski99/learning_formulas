#include "types.hpp"
#include "utils.hpp"
#include "RandomClassifier.hpp"
#include <iostream>
#include <fstream>
#include <ctime>
#include <sstream>

int decision_classes_count = 0;

std::string train_file_name = "../train.txt";
std::string test_file_name = "../test.txt";
int max_cycles_count_param = 20;
int formulas_count_param = 100;
int clauses_count_param = 5;
int literals_count_param = 3;
float positive_responses_percentage = 0.4;
std::string result_dir = "../result/";

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
    stream << result_dir << ms << ".txt";

    clf.saveFormulasToFile(stream.str());

    return 0;
}