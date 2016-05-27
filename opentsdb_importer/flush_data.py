#!/usr/bin/env python3
import sys
import random
import math
import time
import threading

from opentsdb_importer.utils import *
from opentsdb_importer.config import *

# START_TIMESTAMP = datetime_string_to_timestamp("01/01/2000 0:00") # timestamp in second unit

class worker (threading.Thread):
    def __init__(self, threadID, name, start_timestamp, number_data_points, interval,  start_val, end_val, tags):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.start_timestamp = start_timestamp
        self.number_data_points = number_data_points
        self.interval = interval
        self.start_val = start_val
        self.end_val = end_val
        self.tags = tags

    def run(self):
        # print("Starting " + self.name)
        running_timestamp = self.start_timestamp
        count_looping = 0
        for i in range(0,self.number_data_points, MAX_DPPR):
            # Packing data points into a list of JSON
            metrics = []
            for j in range(find_num_dppr(count_looping, \
                           self.number_data_points, \
                           MAX_DPPR)):
                metrics.append({
                    "metric": 'level',
                    "timestamp": running_timestamp,
                    "value": random.randint(self.start_val, self.end_val),
                    "tags": self.tags
                })
                running_timestamp += self.interval
            send_metrics(metrics)
            print(self.name + " timestamp: "+ str(running_timestamp) + " " \
                    + str(i*100/self.number_data_points)+ " %")
            count_looping += 1
        # print("Exiting " + self.name)

def convert_tags_string_to_dict(tags_string):
    result = {}
    tmp = tags_string[0].split('=')
    result[tmp[0]] = tmp[1]
    return result

def find_num_dppr(count_looping, number_data_points, max_dppr):
    # finding the exactly number data points of each loop
    num_looping = math.ceil(number_data_points / max_dppr)
    if count_looping + 1 == num_looping and number_data_points % max_dppr != 0:
        return number_data_points % max_dppr
    return max_dppr

def calculate_scope_of_each_thread(start_timestamp, number_data_points, num_threads, interval):
    result = []
    for thread_id in range(num_threads):
        number_each_thread = int(number_data_points/num_threads)

        if thread_id + 1 == num_threads and number_data_points % num_threads != 0:
            number_each_thread_tmp = number_data_points - number_each_thread * num_threads + number_each_thread
        else:
            number_each_thread_tmp = number_each_thread

        starting_timestamp_each_thread = start_timestamp + int(thread_id*interval*number_each_thread)
        result.append({'num': number_each_thread_tmp, 'start': starting_timestamp_each_thread})
    return result

def flush_data(starting_timestamp, number_data_points, interval, num_threads,  start_val, end_val, tags):
    scopes = calculate_scope_of_each_thread(starting_timestamp, number_data_points, num_threads, interval)
    threads = []
    for i, scope in enumerate(scopes):
        threads.append(worker(i+1, "Thread " + str(i+1), scope['start'], scope['num'], interval,  start_val, end_val, convert_tags_string_to_dict(tags)))
        threads[i].start()

    for thread in threads:
        thread.join()
    return 0

def printInstruction():
    print("flush_data.py [starting_timestamp] [number_of_data_points] [interval] [num_threads] [start_val] [end_val] [[tagk1=tagv1] [tagk2=tagv2]... ]")
    print("Example: flush_data.py 946659600 10000 5 16 5000 6000 location=hatyai")
    print("[starting_timestamp    ] in seconds")
    print("[number_of_data_points ] A number of data points")
    print("[interval              ] in seconds")
    print("[num_threads           ] A number of thread")
    print("")
    print("Scope of data that will bed generated")
    print("Generate from [start_val] to [end_val]")
    print("other is tags of that metric Ex. location=hatyai (w/o space)")

if __name__ == '__main__':
    num_threads = 1
    if len(sys.argv) < 8:
        printInstruction()
        exit()

    starting_timestamp = int(sys.argv[1])
    number_data_points = int(sys.argv[2])
    interval           = int(sys.argv[3])
    num_threads        = int(sys.argv[4])
    start_val          = int(sys.argv[5])
    end_val            = int(sys.argv[6])

    tags = []
    for i in range(7, len(sys.argv)):
        tags.append(sys.argv[i])

    start_time = time.time()
    flush_data(starting_timestamp, number_data_points, interval, num_threads, start_val, end_val, tags)
    print("End flushing %s seconds" % (time.time() - start_time))
