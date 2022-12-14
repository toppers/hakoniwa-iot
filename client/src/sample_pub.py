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

from stub.hakopy import btle
from stub.hakopy.btle import Peripheral
import stub.hakopy.btle as btle
import stub.hakopy.polar as polar
from stub.hakopy.polar import PolarDataReader

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


class MySensor(Peripheral):
    def __init__(self, addr, addrType):
        Peripheral.__init__(self, addr, addrType)

class MyDelegate(btle.DefaultDelegate):
    def __init__(self, params):
        btle.DefaultDelegate.__init__(self)
        self.client = mqtt.Client()
        self.server_port = MQTT_PORT
        self.is_tls = params
        #TLS
        if (self.is_tls):
            self.server_port = MQTT_TLS_PORT
            self.client.tls_set(
                tls_cacert,
                certfile = tls_cert,
                keyfile = tls_key,
                tls_version = ssl.PROTOCOL_TLSv1_2
            )
            self.client.tls_insecure_set(True)

        self.count = 0
        self.client.on_connect = on_connect
        self.client.on_disconnect = on_disconnect
        self.client.connect(server_ipaddr, self.server_port)
        self.client.loop_start()

    def handleNotification(self, cHandle, data):
        self.data = {
            "device_id": "xxxxx-0001",
            "time": '',
            "heart": "0"
        }
        self.data['time'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
        self.data['heart'] = data
        message = json.dumps(self.data)
        print(topic_name + " : " + message)

        self.client.publish(topic_name, message, qos=1)
        self.count = self.count + 1

def main(is_tls, reader):
    sensor = MySensor("dumy", "public")
    sensor.setDelegate(MyDelegate(is_tls))

    ####### stub code ###############
    sensor.setReader(reader)
    #################################

    LoopFlag = True
    while LoopFlag:
        try:
            if sensor.waitForNotifications(1.0):
                #print('handleNotification() was called')
                continue
        except Exception as e:
            print("Other error occurs: {}".format(e))
            break

if __name__ == "__main__":
    is_tls = False
    if (len(sys.argv) == 3):
        is_tls = True
    sample_data=sys.argv[1]
    print("data=" + sample_data)
    print("tls=" + str(is_tls))

    ####### stub code ###############
    polar_reader = PolarDataReader(sample_data) 
    #################################

    main(is_tls, polar_reader)