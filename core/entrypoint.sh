#!/bin/bash

if [ "${ALGORITHM}" == "RANDOM" ]; then
    exec "./learning_formulas" \
        "${TRAIN_FILE_NAME}" \
        "${TEST_FILE_NAME}" \
        "${ALGORITHM}" \
        "${CLAUSES_COUNT_CONSTANT}" \
        "${LITERALS_COUNT_CONSTANT}" \
        "${CYCLES_COUNT}" \
        "${FORMULAS_COUNT}" \
        "${CLAUSES_COUNT}" \
        "${LITERALS_COUNT}" \
        "${POSITIVE_RESPONSES_PERCENTAGE}"
fi
