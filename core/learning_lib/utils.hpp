#include "types.hpp"
#include <vector>
#include <iostream>
#include <string>
#include <sstream>

void setSrandTime();

int randomInt(int min, int max);

void displayLiteral(Literal literal);

void displayFormula(Formula formula);

std::string stringifyFormula(Formula formula);

Formula fromString(std::string pattern);

std::vector<string> split(std::string word, std::string delimiter);