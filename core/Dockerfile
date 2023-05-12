FROM ubuntu:latest

ENV TRAIN_FILE_NAME="train.txt"
ENV TEST_FILE_NAME="test.txt"
ENV CYCLES_COUNT=20
ENV FORMULAS_COUNT=200
ENV CLAUSES_COUNT=6
ENV LITERALS_COUNT=3
ENV POSITIVE_RESPONSES_PERCENTAGE=0.4

WORKDIR /src

RUN apt-get update && apt-get install -y \
    build-essential \
    gcc \
    cmake 

COPY . /src

WORKDIR /src/build 

RUN cmake .. && make

CMD ["sh", "-c", "./learning_formulas ${TRAIN_FILE_NAME} ${TEST_FILE_NAME} ${CYCLES_COUNT} ${FORMULAS_COUNT} ${CLAUSES_COUNT} ${LITERALS_COUNT} ${POSITIVE_RESPONSES_PERCENTAGE}"]


