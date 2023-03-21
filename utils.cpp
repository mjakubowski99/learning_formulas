#include "types.hpp"
#include "utils.hpp"
#include <iostream>
#include <string>
#include <sstream>
#include <cstring>

void displayLiteral(Literal literal) {
    if (!literal.positive) {
        std::cout << "~";
    }
    std::cout << "X" << literal.bitPosition;
}

void displayFormula(Formula formula)
{
    for(Clause clause : formula) {
        std::cout << "(";
        for(Literal literal : clause) {
            displayLiteral(literal);
            std::cout << " v ";
        }
        std::cout << ") ^ \n";
    }
}

std::string stringifyFormula(Formula formula)
{
    std::stringstream ss("");

    int i = 0;
    for(Clause clause : formula) {
        ss << "(";

        int j=0;
        for(Literal literal : clause) {
            if (!literal.positive) {
                ss << "~";
            }
            ss << "X" << literal.bitPosition;

            if (j<clause.size()-1) {
                ss << "v";
            }
            j++;
        }
        ss << ")";
        if (i<formula.size()-1) {
            ss << "^";
        }
        i++;
    }

    return ss.str();
}

Formula fromString(std::string pattern)
{
    Formula formula;

    vector<string> clauses = split(pattern, "^");

    for(string clause : clauses) {
        Clause result_clause;

        clause = clause.substr(1,clause.size()-1);
        vector<string> literals = split(clause,"v");

        for(string literal : literals) {
            Literal result_literal;
            if (literal.substr(0,2) == "~X") {
                result_literal.positive = false;
            } else if (literal.substr(0,1) == "X"){
                result_literal.positive = true;
            } else {
                throw "Failed to parse formula from string";
            }
            result_literal.bitPosition = atoi("");

            result_clause.push_back(result_literal);
        }
        formula.push_back(result_clause);
    }
    return formula;
}

std::vector<string> split(std::string word, std::string delimiter)
{
    std::vector<string> result;

    char * chr = new char[word.length()+1];
    strcpy(chr, word.c_str());

    char * dlm = new char[delimiter.length()+1];
    strcpy(dlm, delimiter.c_str());

    char * tokenized = strtok(chr, dlm);
    
    while(tokenized != NULL) {
        result.push_back(tokenized);
        tokenized = strtok(NULL, dlm);
    }

    return result;
}
