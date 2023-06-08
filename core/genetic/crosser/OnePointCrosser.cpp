#include "OnePointCrosser.hpp"
#include "../../utils.hpp"

Formula OnePointCrosser::cross(Formula & a, Formula & b)
{
    Formula result;

    if (a.size() < b.size()) {
        return run(a,b);
    }
    return run(b,a);
}

Formula OnePointCrosser::run(Formula & a, Formula & b)
{
    int clause_split_point = randomInt(0, a.size());
    int literal_split_point = randomInt(0, a[clause_split_point].size());

    for(int i=clause_split_point; i<b.size(); i++) {
        for(int j=literal_split_point; j<b[i].size(); j++) {

            if (i<clause_split_point) {
                b[i] = a[i];
            }
            if (i==clause_split_point && j<literal_split_point) {
                a[i][j] = b[i][j];
            }
        }
    }

    return b;
}