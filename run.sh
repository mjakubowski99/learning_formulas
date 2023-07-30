#!/bin/bash

cd core 

if [ -d "build" ] 
then
    cd build 
    echo "Build cached!" 
else
    mkdir build && cd build
    cmake .. && make
fi

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
    $MUTATION_PERCENTAGE \
    $REPRODUCTION_PERCENTAGE \
    $KEEP_BEST
