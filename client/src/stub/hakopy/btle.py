#!/usr/bin/env python

import time

class BTLEException(Exception):
    def __init__(self, msg, resp_dict=None):
        self.msg = msg

    def __str__(self):
        str_msgs = self.msg
        return str_msgs

class DefaultDelegate:
    def __init__(self):
        pass

    def handleNotification(self, cHandle, data):
        pass

    def handleNotification(self, cHandle, data):
        pass


class Peripheral:
    def __init__(self, deviceAddr=None, addrType="public", iface=None, timeout=None):
        self.status = "disc"
        self.delegate = None
        (self.deviceAddr, self.addrType, self.iface) = (None, None, None)
        if deviceAddr is not None:
            self.connect(deviceAddr, addrType, iface, timeout)

    def setDelegate(self, delegate_):
        self.delegate = delegate_

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.disconnect()

    def connect(self, addr, addrType="public", iface=None, timeout=None):
        self.status = "conn"
        self.addr = addr
        self.addrType = addrType
        self.iface = iface

    def disconnect(self):
        self.setDelegate(None)
        self.status = "disc"

    def getState(self):
        return self.status

    def getServices(self):
        return None

    def readCharacteristic(self, handle):
        return "dummy data"

    def writeCharacteristic(self, handle, val, withResponse=False, timeout=None):
        return 0

    def waitForNotifications(self, timeout):
        time.sleep(timeout)
        self.delegate.handleNotification(0x00, "dummy data")

    def __del__(self):
        self.disconnect()
