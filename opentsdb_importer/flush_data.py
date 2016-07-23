import sys
import os
import random
import math
import time
import threading
import queue

from opentsdb_importer.utils import *
from opentsdb_importer.config import *

# START_TIMESTAMP = datetime_string_to_timestamp("01/01/2000 0:00") # timestamp in second unit

# Threading in python: retrieve return value when using target
# http://stackoverflow.com/questions/2577233/threading-in-python-retrieve-return-value-when-using-target
class DataGeneratorWorker (threading.Thread):
    # TODO: support more than one tag
    # def __init__(self, threadID, name, start_timestamp, number_data_points, interval,  start_val, end_val, tags):
    # --- worker_configs ---
    # worker_configs = {
    #     "starting_timestamp": 0,
    #     "number_data_points" : 0,
    #     "interval": 0,
    #     "start_val": 0,
    #     "end_val": 0,
    #     "tags": 0
    # }

    def __init__(self, threadID, worker_configs, q):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.q = q
        for (prop, value) in worker_configs.items():
            setattr(self, prop, value)

    def run(self):
        total_dps = 0
        # print("Starting " + self.threadID)
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
            write_adapter(metrics, self.threadID, self.write_mode)
            total_dps += len(metrics)
            # print(str(self.threadID) + " timestamp: "+ str(running_timestamp) + " " \
            #         + str(i*100/self.number_data_points)+ " %")
            count_looping += 1
        self.q.put(total_dps)
        # print("Exiting " + self.threadID)

class DataGenerator(object):
    # TODO: support more than one tag

    def __init__(self, **kwargs):
        prop_defaults = {
            "write_mode": None,
            "start_timestamp": 946659600,
            "number_data_points" : 10000,
            "interval": 5,
            "num_threads": 2,
            "start_val": 5000,
            "end_val": 6000,
            "tags": [
                "location=hatyai"
            ]
        }

        for (prop, default) in prop_defaults.items():
            setattr(self, prop, kwargs.get(prop, default))

    def run(self):
        # flush_data
        scopes = calculate_scope_of_each_thread(self.start_timestamp, \
                                                self.number_data_points, \
                                                self.num_threads, \
                                                self.interval)

        threads = []
        q = queue.Queue()
        for i, scope in enumerate(scopes):
            worker_configs = {
                "write_mode": self.write_mode,
                "start_timestamp": scope['start'],
                "number_data_points" : scope['num'],
                "interval": self.interval,
                "start_val": self.start_val,
                "end_val": self.end_val,
                "tags": convert_tags_string_to_dict(self.tags)
            }
            threads.append(DataGeneratorWorker(threadID = i+1, \
                                               worker_configs = worker_configs, \
                                               q = q))
            threads[i].start()
        for thread in threads:
            thread.join()

        total_dps = 0
        for thread in threads:
            total_dps += int(q.get())
        return total_dps

# Utils Functions

def convert_tags_string_to_dict(tags_string):
    # TODO: support more than one tag
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

# def prepare_target_directory():
#     # add counter when prefix directory is duplicate
#     current_times = 0
#     prefix = 'datapoints'
#     for item in os.listdir():
#         if prefix in item and prefix is not item:
#             print(item)
#             tmp = item.split('-')
#             current_times = int(tmp[1])
#     current_times += 1
#     target_directory = '%s-%d' % (prefix, current_times)
#     if not os.path.exists(target_directory):
#         os.makedirs(target_directory)
#     return target_directory

def write_to_file(metrics, threadID):
    target_directory = "generated-dps"
    if not os.path.exists(target_directory):
        os.makedirs(target_directory)
    f = open('%s/dps-%d' % (target_directory, threadID )  , 'a')
    for metric in metrics:
        f.write('%s %d %d' % (metric['metric'], metric['timestamp'], metric['value']))
        for key, value in metric['tags'].items():
            f.write(' %s=%s' % (key, value))
        f.write('\n')
    f.close()
    # print("%d) number of metrics: %d" % (threadID, len(metrics)))

def write_adapter(metrics, threadID, adapter_type=None):
    # adapter_type: file, opentsdb
    if adapter_type == "file":
        write_to_file(metrics, threadID)
    elif adapter_type == "opentsdb":
        send_metrics(metrics)
    else:
        print("No print anything")
