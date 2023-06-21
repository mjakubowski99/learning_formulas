#include "OnePointCrosser.hpp"
#include "../../utils.hpp"

Formula OnePointCrosser::cross(Formula & a, Formula & b)
{
    Formula result;
    int clause_from_a = randomInt(0, a.size());
    int clasuse_from_b = randomInt(0, b.size());

    if (randomInt(0,2)%2==0) {
        a[clause_from_a] = b[clasuse_from_b];
        return a;
    }
    else {
        b[clasuse_from_b] = a[clause_from_a];
        return b;
    }
}