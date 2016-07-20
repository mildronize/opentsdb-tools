import time
import datetime
import requests
import json
import random
import sys
# I/O

from opentsdb_importer.config import *

def send_metric(metric,  value, tags, timestamp=int(time.time()) ):
    url = 'http://'+SERVER_IP+':'+SERVER_PORT+'/api/put?details'
    data = {
        "metric": metric,
        "timestamp": timestamp,
        "value": value,
        "tags":  tags
    }
    # print(json.dumps(data))
    r = requests.post(url, data = json.dumps(data))
    if r.status_code != requests.codes.ok:
        print("Error! " + str(r.status_code))
        print(r.text)
        exit(1)

def send_metrics(data):
    f = open("/tmp/flush_error", 'a')
    url = 'http://'+SERVER_IP+':'+SERVER_PORT+'/api/put?details'
    num_try = 0
    is_give_up = True
    while num_try < NUM_TRY:
        try:
            r = requests.post(url, data = json.dumps(data))
            if r.status_code != requests.codes.ok:
                print("Error! " + str(r.status_code))
                print(r.text)
                # print('----- Trace Data ---------')
                # print(json.dumps(data))
                exit(1)
            is_give_up = False
            break
        except OSError as err:
            f.write("OS error: {0}".format(err) + "\n")
        except:
            f.write("Unexpected error:", sys.exc_info()[0] + "\n")
            raise
        time.sleep(TIME_DELAY_BEFORE_TRY_NEW_FLUSH)
        num_try += 1
    
    if is_give_up:
        exit(1)

    f.close()


def datetime_string_to_timestamp(datetime_string):
    """input string date -> 13/10/2015 0:45
    expected result ->  1444697100 """
    return int(time.mktime(datetime.datetime.strptime(\
        datetime_string,"%d/%m/%Y %H:%M").timetuple()))
