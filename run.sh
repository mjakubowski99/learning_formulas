#!/bin/bash

input=".env"
while IFS= read -r line
do
    export "$line"
done < "$input"

cd ../core

mkdir -p build && cd build
cmake .. && make

./learning_formulas \
    $TRAIN_FILE_NAME \
    $TEST_FILE_NAME \
    $RESULT_DIR \
    $ALGORITHM \
    $MIN_CLAUSES_COUNT \
    $MAX_CLAUSES_COUNT \
    $MIN_LITERALS_COUNT \
    $MAX_LITERALS_COUNT \
    $POPULATIONS_COUNT \
    $POPULATIONS_SIZE \
    $FINAL_POPULATION_SIZE \
    $NEW_FORMULAS_PERCENTAGE \
    $CROSSING_PERCENTAGE
