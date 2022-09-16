#!/bin/bash

if [ $# -ne 1 -a $# -ne 2 ]
then
    echo "Usage: $0 <message> [tls]"
    exit 1
fi

if [ $# -eq 1 ]
then
    mosquitto_pub -h ${BROKER_IPADDR} -d  -t topicA -m "${1}" -p 1883
else
    mosquitto_pub -h ${BROKER_IPADDR} -d  -t topicA -m "${1}" -p 8883 --cafile ./config/tls/server.crt --tls-version tlsv1.2
fi
