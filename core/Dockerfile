FROM ubuntu:latest

ENV FILE_NAME="../train.txt"
ENV CYCLES_COUNT=10
ENV FORMULAS_COUNT=100
ENV CLAUSES_COUNT=6
ENV LITERALS_COUNT=3

WORKDIR /src

RUN apt-get update && apt-get install -y \
    build-essential \
    gcc \
    cmake 

COPY . /src 

WORKDIR /src/build 

RUN cmake .. && make 

CMD ["./learning_formulas"]


