#pragma once

#include <deque>
#include <vector>
#include <list>
#include <array>
#include <set>
#include <list>
#include <algorithm>
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

typedef vector<Clause> Formula;

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
    bool ** data;
    Data();
    Data(int rows_count, int attributes_count);
    void init(int rows);
    void insert(int i, int j, bool value);
    bool get(int i, int j);
};

#endif

#ifndef FORMULA_WITH_SCORE
#define FORMULA_WITH_SCORE

struct FormulaWithScore
{
    float score;
    Formula formula;
};

#endif

#ifndef FORMULA_WITH_SCORE_ARRAY
#define FORMULA_WITH_SCORE_ARRAY

struct FormulaWithScoreArray
{
    FormulaWithScore * formulas;
    int size=0;

    FormulaWithScoreArray(){};

    FormulaWithScoreArray(int size)
    {
        this->formulas = new FormulaWithScore[size];
        this->size = size;
    }

    void sortByScore()
    {
        sort(this->formulas, this->formulas+this->size, [](FormulaWithScore & a, FormulaWithScore & b) {return a.score > b.score;});
    }
};

#endif 
