FROM ubuntu:latest

WORKDIR /src

RUN apt-get update && apt-get install -y \
    build-essential \
    gcc \
    cmake 

COPY . /src

WORKDIR /src/build 

RUN cmake .. && make

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ENTRYPOINT [ "/entrypoint.sh" ]


