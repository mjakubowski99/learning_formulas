#include "types.hpp"

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
    this->data = new bool*[this->rows_count];
    for(int i=0; i<this->attributes_count; i++) {
        this->data[i] = new bool[this->attributes_count];
    }
}

void Data::fromVector(std::vector<std::vector<bool>> vec)
{
    for(int i=0; i<this->rows_count; i++) {
        for(int j=0; j<this->attributes_count; j++) {
            this->data[i][j] = vec[i][j];
        }
    }
}

FormulaScore::FormulaScore()
{
    this->true_positives = 0;
    this->true_negatives = 0;
    this->false_positives = 0;
    this->false_negatives = 0;
}

FormulaScore FormulaScore::operator+(const FormulaScore & score)
{
    this->true_positives = score.true_positives;
    this->true_negatives = score.true_negatives;
    this->false_positives = score.false_negatives;
    this->false_negatives = score.false_negatives;
}