#!/bin/bash

if [ "${ALGORITHM}" == "RANDOM" ]; then
    exec "./learning_formulas" \
        "${TRAIN_FILE_NAME}" \
        "${TEST_FILE_NAME}" \
        "${RESULT_DIR}" \
        "${ALGORITHM}" \
        "${MIN_CLAUSES_COUNT}" \
        "${MAX_CLAUSES_COUNT}" \
        "${MIN_LITERALS_COUNT}" \
        "${MAX_LITERALS_COUNT}" \
        "${CYCLES_COUNT}" \
        "${FORMULAS_COUNT}" \
        "${POSITIVE_RESPONSES_PERCENTAGE}"
fi

if [ "${ALGORITHM}" == "EVOLUTION" ]; then
    exec "./learning_formulas" \
        "${TRAIN_FILE_NAME}" \
        "${TEST_FILE_NAME}" \
        "${RESULT_DIR}" \
        "${ALGORITHM}" \
        "${MIN_CLAUSES_COUNT}" \
        "${MAX_CLAUSES_COUNT}" \
        "${MIN_LITERALS_COUNT}" \
        "${MAX_LITERALS_COUNT}" \
        "${POPULATIONS_COUNT}" \
        "${POPULATIONS_SIZE}" \
        "${FINAL_POPULATION_SIZE}" \
        "${MUTATION_PERCENTAGE}" \
        "${REPRODUCTION_PERCENTAGE}"
fi

