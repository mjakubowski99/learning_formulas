#pragma once

#include <deque>
#include <vector>
#include <list>
using namespace std;


#ifndef LITERAL_H
#define LITERAL_H

struct Literal {
    int bitPosition;
    bool positive;

    Literal(int bitPositon, bool positive);
};

#endif

#ifndef FORMULA_SCORE_H
#define FORMULA_SCORE_H

struct FormulaScore {
    int true_positives;
    int true_negatives;
    int false_positives;
    int false_negatives;
};

#endif

#ifndef CLAUSE_H
#define CLAUSE_H

typedef vector<Literal> Clause;

#endif

#ifndef FORMULA_H
#define FORMULA_H

typedef deque<Clause> Formula;

#endif

#ifndef FORMULA_VOTE_H
#define FORMULA_VOTE_H

struct FormulaVote
{
    std::list<Formula> positive;
    std::list<Formula> negative;
};

#endif

#ifndef ROW_H
#define ROW_H

typedef vector<bool> Row;

#endif

#ifndef DATAFRAME_H
#define DATAFRAME_H

typedef vector<Row> Dataframe;

#endif

