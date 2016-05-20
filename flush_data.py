#!/usr/bin/env python3
import sys

import csv
import time
import datetime

import random

import threading

from utils import *


START_TIMESTAMP = datetime_string_to_timestamp("01/01/2000 0:00") # timestamp in second unit
INTERVAL = 5 # seconds

NUM_TRY = 5 # times
TIME_DELAY_BEFORE_TRY_NEW_FLUSH = 5 # seconds

NUM_DATA_POINTS_PER_REQUEST = 100 # data points

class worker (threading.Thread):
    def __init__(self, threadID, name, start_timestamp, number_data_points):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.start_timestamp = start_timestamp
        self.number_data_points = number_data_points

        print(start_timestamp, number_data_points)

    def run(self):
        print("Starting " + self.name)
        running_timestamp = self.start_timestamp
        for i in range(self.number_data_points):
            num_try = 0
            while num_try < NUM_TRY:
                print(self.name + " timestamp: "+ str(running_timestamp) + " " + str(i/self.number_data_points*100)+ " %")
                try:
                    send_metric(metric='level', \
                                timestamp = running_timestamp, \
                                value = value_generator(5000, 6000), \
                                tags = {'location':'hatyai'}
                    )
                    running_timestamp += INTERVAL
                    break
                except OSError as err:
                    print("OS error: {0}".format(err))
                except:
                    print("Unexpected error:", sys.exc_info()[0])
                    raise
                time.sleep(TIME_DELAY_BEFORE_TRY_NEW_FLUSH)
                num_try += 1
        print("Exiting " + self.name)

def value_generator(start, end):
    return random.randint(start, end)

def thread_scopes(start_timestamp, number_data_points, num_threads):
    result = []
    print(start_timestamp)
    for thread_id in range(num_threads):
        number_each_thread = int(number_data_points/num_threads)

        if thread_id + 1 == num_threads and number_data_points % num_threads != 0:
            number_each_thread_tmp = number_data_points - number_each_thread * num_threads + number_each_thread
        else:
            number_each_thread_tmp = number_each_thread

        starting_timestamp_each_thread = start_timestamp + int(thread_id*INTERVAL*number_each_thread)
        result.append({'num': number_each_thread_tmp, 'start': starting_timestamp_each_thread})
    return result

def flush_data(number_data_points, num_threads):
    scopes = thread_scopes(START_TIMESTAMP, number_data_points, num_threads)
    threads = []
    for i, scope in enumerate(scopes):
        print("flush ",scope['start'], scope['num'])
        threads.append(worker(i+1, "Thread " + str(i+1), scope['start'], scope['num']))
        threads[i].start()

    for thread in threads:
        thread.join()
    return 0

# def simple_flush_data(number_data_points):
#     running_timestamp = START_TIMESTAMP
#     for i in range(number_data_points):
#         print(str(i)+" timestamp: "+ str(running_timestamp) + " " + str(i/number_data_points*100)+ " %")
#         send_metric(metric='level', \
#                     timestamp = running_timestamp, \
#                     value = value_generator(5000, 6000), \
#                     tags = {'location':'hatyai'}
#         )
#         running_timestamp += INTERVAL
#     return 0

def printInstruction():
    print("flush_data.py [number_of_data_points] [num_threads]")
    pass

if __name__ == '__main__':
    num_threads = 1
    if len(sys.argv) < 2:
        printInstruction()
        exit()
    elif len(sys.argv) == 3:
        num_threads = int(sys.argv[2])
    elif len(sys.argv) > 3:
        printInstruction()
        exit()

    number_data_points = int(sys.argv[1])
    start_time = time.time()
    # if num_threads == 1:
    #     simple_flush_data(number_data_points)
    # else:
    flush_data(number_data_points, num_threads)
    print("End flushing %s seconds" % (time.time() - start_time))
