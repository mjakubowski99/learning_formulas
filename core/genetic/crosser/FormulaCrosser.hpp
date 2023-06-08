#pragma once 

#include "../../types.hpp"

class FormulaCrosser {
    public:
        virtual Formula cross(Formula & a, Formula & b) = 0;
};