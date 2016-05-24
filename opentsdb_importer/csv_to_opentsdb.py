#!/usr/bin/env python3
import sys
import csv

from opentsdb_importer.utils import *

def count_csv_line(path):
    with open(path, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        return len(list(reader))

def read_csv(path):
    #  timestamp_old = 0
    with open(path, 'r',encoding="utf-8") as f:
        reader = csv.reader(f)
        num_row = count_csv_line(path)
        i = 0
        for row in reader:
            if i > 1:
               result = row_convert(row)
               #  if result[0] != timestamp_old:
               #  timestamp_old = result[0]
               #  metrics.send('level', result[])
               send_metric( metric = 'level', \
                       timestamp = result[0], \
                       value =  result[1], \
                       tags= {'location':'klong_luek'})
               print('%d ' % (i*100/num_row))
            i += 1

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
    datetime_string = pad_zero_datetime(row[0])
    timestamp = datetime_string_to_timestamp(datetime_string)
    return [timestamp, int(row[1])]

def printInstruction():
    print("")
    print("usage: csv_to_openstdb.py [path]")

if __name__ == '__main__':
    if len(sys.argv) != 2:
        printInstruction()
        exit()

    path = sys.argv[1]
    read_csv(path)
