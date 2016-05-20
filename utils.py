import time
import datetime
import requests
import json
# I/O

NUM_TRY = 5 # times
TIME_DELAY_BEFORE_TRY_NEW_FLUSH = 5 # seconds

def send_metric(metric,  value, tags, timestamp=int(time.time()) ):
    url = 'http://127.0.0.1:4242/api/put?details'
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
    url = 'http://127.0.0.1:4242/api/put?details'
    num_try = 0
    while num_try < NUM_TRY:
        try:
            r = requests.post(url, data = json.dumps(data))
            if r.status_code != requests.codes.ok:
                print("Error! " + str(r.status_code))
                print(r.text)
                # print('----- Trace Data ---------')
                # print(json.dumps(data))
                exit(1)
            break
        except OSError as err:
            print("OS error: {0}".format(err))
        except:
            print("Unexpected error:", sys.exc_info()[0])
            raise
        time.sleep(TIME_DELAY_BEFORE_TRY_NEW_FLUSH)
        num_try += 1

def datetime_string_to_timestamp(datetime_string):
    """input string date -> 13/10/2015 0:45
    expected result ->  1444697100 """
    return int(time.mktime(datetime.datetime.strptime(\
        datetime_string,"%d/%m/%Y %H:%M").timetuple()))
