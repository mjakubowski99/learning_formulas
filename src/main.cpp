#include "formulas/formulas.hpp"
#include "classifier/classifier.hpp"
#include <iostream>
#include <fstream>
#include <sstream>
#include <string>
#include <map>

std::map<int, Dataframe> getData(std::string file_name)
{
    std::ifstream file;
    file.open("../src/test.txt");

    std::map<int, Dataframe> data;

    std::string line;
    while(getline(file,line))
    {
        std::stringstream linestream(line);
        std::string value;

        Row row;
        while(getline(linestream,value,','))
        {
            row.push_back(value=="0" ? false : true);
        }

        int back = row.back();
        row.pop_back();

        if (back == true) {
            data[1].push_back(row);
        } else {
            data[0].push_back(row);
        }
    }

    file.close();

    return data;
}

int main() {
    std::string train_file = "../scr/train.txt";
    std::string test_file = "../src/test.txt";
    
    std::map<int, Dataframe> train_data = getData(train_file);
    std::map<int, Dataframe> test_data = getData(test_file);

    Classifier classifier(20, 50, 10, 4);

    classifier.fit(train_data);

    std::cout << classifier.score(test_data) << std::endl;

    return 0;
}