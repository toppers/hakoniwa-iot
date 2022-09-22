#!/usr/bin/env python

import csv

class PolarDataReader:
    def __init__(self, filepath):
        self.file = open(filepath)
        self.csv_reader = csv.reader(self.file)
        # skip head line
        head = next(self.csv_reader)
        print("head=" + head[0])

    def readData(self):
        data = next(self.csv_reader)
        return data[2]

