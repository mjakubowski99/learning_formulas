#include "types.hpp"
#include <set>

Literal::Literal(){}

Literal::Literal(int bitPosition, bool positive)
{
    this->bitPosition = bitPosition;
    this->positive = positive;
}

Data::Data()
{
    this->rows_count = 0;
    this->attributes_count = 0;
}

Data::Data(int rows_count, int attributes_count)
{
    this->rows_count = rows_count;
    this->attributes_count = attributes_count;
    this->data = new bool*[rows_count];
    for(int i=0; i<rows_count; i++){
        this->data[i] = new bool[attributes_count];
    }
}

void Data::init(int rows)
{
    this->data = new bool*[rows];
}

void Data::insert(int i, int j, bool value)
{
    this->data[i][j] = value;
}

bool Data::get(int i, int j)
{
    return this->data[i][j];
}

FormulaScore::FormulaScore()
{
    this->true_positives = 0;
    this->true_negatives = 0;
    this->false_positives = 0;
    this->false_negatives = 0;
}

FormulaScore & FormulaScore::operator+(const FormulaScore & score)
{
    this->true_positives += score.true_positives;
    this->true_negatives += score.true_negatives;
    this->false_positives += score.false_positives;
    this->false_negatives += score.false_negatives;
    return *this;
}