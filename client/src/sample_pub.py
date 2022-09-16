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
MQTT_PORT = 1883
MQTT_TLS_PORT = 8883
topic_name = "topicA"

tls_cacert = './config/tls/server.crt'
tls_cert = './config/tls/client.crt'
tls_key = './config/tls/client.key'

def on_connect(unused_client, unused_userdata, unused_flags, rc):
    print("on_connect:", mqtt.connack_string(rc))

def on_disconnect(unused_client, unused_userdata, unused_flags, rc):
    print("on_disconnect:", error_str(rc))



def main(is_tls):
    client = mqtt.Client()

    server_port = MQTT_PORT
    #TLS
    if (is_tls):
        server_port = MQTT_TLS_PORT
        client.tls_set(
            tls_cacert,
            certfile = tls_cert,
            keyfile = tls_key,
            tls_version = ssl.PROTOCOL_TLSv1_2
        )
        client.tls_insecure_set(True)

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
    is_tls = False
    if (len(sys.argv) == 2):
        is_tls = True
    print("tls=" + str(is_tls))
    main(is_tls)