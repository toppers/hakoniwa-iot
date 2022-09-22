#!/bin/bash

if [ $# -ne 1 ]
then
    echo "Usage: $0 output"
    exit 1
fi
OUTPUT=${1}

tcpdump -i eth0 -X -s 0 -w ${OUTPUT}
