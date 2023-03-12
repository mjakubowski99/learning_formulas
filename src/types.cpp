#include "types.hpp"

Literal::Literal(int bitPosition, bool positive)
{
    this->bitPosition = bitPosition;
    this->positive = positive;
}