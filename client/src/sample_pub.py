# -*- coding: utf-8 -*-
import binascii
import time
import paho.mqtt.client as mqtt
from datetime import datetime
import json

import argparse
import os
import sys
import datetime
import jwt
import ssl

server_ipaddr = "192.168.11.4"
server_port = 1883
topic_name = "topicA"


def on_connect(unused_client, unused_userdata, unused_flags, rc):
    print("on_connect:", mqtt.connack_string(rc))

def on_disconnect(unused_client, unused_userdata, unused_flags, rc):
    print("on_disconnect:", error_str(rc))



def main():
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_disconnect = on_disconnect

    client.connect(server_ipaddr, server_port)
    client.loop_start()

    data = {
        "timestamp": '',
        "count": 0,
        "message": "hello world!"
    }
    count = 0
    LoopFlag = True
    while LoopFlag:
        try:
            data['timestamp'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
            data['count'] = count
            message = json.dumps(data)
            print("message=", message)

            client.publish(topic_name, message, qos=1)
            count = count + 1
        except Exception as e:
            print("Other error occurs: {}".format(e))
            break
        time.sleep(1)

if __name__ == "__main__":
    main()