FROM ubuntu:latest

ARG FILE_NAME
ARG CYCLES_COUNT
ARG FORMULAS_COUNT
ARG CLAUSES_COUNT
ARG LITERALS_COUNT

WORKDIR /src

RUN apt-get update && apt-get install -y \
    build-essential \
    gcc \
    cmake 

COPY . /src 

WORKDIR /src/build 

RUN cmake .. && make

CMD ["./learning_formulas", "${FILE_NAME} ${CYCLES_COUNT} ${FORMULAS_COUNT} ${CLAUSES_COUNT} ${LITERALS_COUNT}"]


