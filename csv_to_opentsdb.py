#!/usr/bin/env python3
import csv
import time
import datetime

def read_csv():
    pass

def pad_zero_time(string_time):
    hours = int(string_time.split(':')[0])
    if hours < 10:
        return '0'+string_time
    return string_time

def pad_zero_date(string_date):
    date_number = int(string_date.split('/')[0])
    if date_number < 10:
        return '0'+string_date
    return string_date

def pad_zero_datetime(string_datetime):
    tmp = string_datetime.split(' ')
    return pad_zero_date(tmp[0]) + ' ' + pad_zero_time(tmp[1])

def row_convert(row):
    """input string date -> 13/10/2015 0:45
    expected result ->  1444697100 """
    time_string = pad_zero_datetime(row[0])
    timestamp = int(time.mktime(datetime.datetime.strptime(\
        time_string,"%d/%m/%Y %H:%M").timetuple()))
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
