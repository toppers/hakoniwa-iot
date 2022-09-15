#!/bin/bash

if [ $# -ne 1 ]
then
    echo "Usage: $0 <message>"
    exit 1
fi

mosquitto_pub -h ${BROKER_IPADDR} -d  -t topicA -m "${1}"
