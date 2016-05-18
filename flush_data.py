#!/usr/bin/env python3
import sys

import csv
import time
import datetime

import requests
import json

from csv_to_opentsdb import metric_send

START_TIME = 

def flush_data(number_data_points):
    return 0



def printInstruction():
    pass

if __name__ == '__main__':
    if len(sys.argv) != 2:
        printInstruction()
        exit()

    number_data_points = int(sys.argv[1])
    flush_data(number_data_points)
