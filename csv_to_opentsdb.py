#!/usr/bin/env python3
import csv
import time
import datetime

def add(a,b):
    return 2;

def read_csv():
    pass

def row_convert(row):
    """input string date -> 13/10/2015 0:45
    expected result ->  1444697100 """
    time_string = row[0]
    timestamp = time.mktime(datetime.datetime.strptime(time_string, "%d-%m-%Y %H:%M").timetuple())
    return [timestamp, int(row[1])]

def start(path):
    with open(path, 'r',encoding="utf-8") as f:
        reader = csv.reader(f)
        i = 0
        for row in reader:
            if i > 1:
               result = row_convert(row)
            i += 1

def printInstruction():
    print("")
    print("usage: csv_to_openstdb.py [path]")

if __name__ == '__main__':
    if len(sys.argv) != 2:
        printInstruction()
        exit()

    path = sys.argv[1]

    start(path)
