FROM ubuntu:20.04

RUN apt-get update
RUN apt-get -y install locales && \
    localedef -f UTF-8 -i ja_JP ja_JP.UTF-8
ENV LANG ja_JP.UTF-8
ENV LANGUAGE ja_JP:ja
ENV LC_ALL ja_JP.UTF-8
ENV TZ JST-9
ENV TERM xterm

RUN apt update -y && apt upgrade -y && apt install -y tcpdump
RUN apt install -y iputils-ping net-tools
RUN apt-get install -y python3-pip
RUN pip install paho-mqtt
RUN apt-get install -y curl

RUN apt update
RUN apt install -y mosquitto mosquitto-clients
RUN pip3 install jwt

