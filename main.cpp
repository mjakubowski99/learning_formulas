#include "types.hpp"
#include "utils.hpp"
#include <iostream>
#include <string>

int main() {
    std::string formula = "(X1vX2)^(X2vX3)";

    std::cout << stringifyFormula(fromString(formula));

    return 0;
}