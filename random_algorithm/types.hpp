#pragma once

#include <deque>
#include <vector>
#include <list>
#include <array>
#include <set>
using namespace std;


#ifndef LITERAL_H
#define LITERAL_H

struct Literal {
    int bitPosition;
    bool positive;

    Literal();
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

    FormulaScore();
    FormulaScore & operator+(const FormulaScore & score);
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

struct DecisionClass
{
    int class_index;

    std::list<Formula> positive_formulas;
    std::list<Formula> negative_formulas;
};

#endif


#ifndef DATA_H
#define DATA_H

struct Data {
    int rows_count;
    int attributes_count;
    std::map<int, bool> data;
    Data();
    Data(int rows_count, int attributes_count);
    void fromVector(std::vector<std::vector<bool>> vec);
};

#endif

