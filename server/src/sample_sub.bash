#!/bin/bash

IS_EXIT=0
cleanup() {
    echo "Trapped signal: $1"
    ps a | grep mosquitto | grep -v grep | awk '{print $1}' | xargs kill -s TERM

    IS_EXIT=1
}

trap_sig() {
    for sig ; do
        trap "cleanup $sig" "$sig"
    done
}

trap_sig INT TERM ERR EXIT PIPE

echo "START"

if [ $# -eq 1 ]
then
    mosquitto -c ./config/mosquitto.conf &
    sleep 3
    mosquitto_sub -h 192.168.11.4 -t topicA  -p 8883 --cafile ./config/tls/server.crt &
else
    mosquitto &
    sleep 3
    mosquitto_sub -h 192.168.11.4 -t topicA &
fi
echo "OK"

while [ 1 ]
do
    C=`ps aux | grep mosquitto | grep -v grep | wc -l`
    if [ $C -eq 0 ]
    then
        break;
    fi
    sleep 1
done

echo "EXIT"
exit 0