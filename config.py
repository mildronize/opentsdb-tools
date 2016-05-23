SERVER_IP   = "127.0.0.1"
SERVER_PORT = "4242"

# "send_metrics" config for trying to resend(reflush) the data again
NUM_TRY                         = 5 # times
TIME_DELAY_BEFORE_TRY_NEW_FLUSH = 5 # seconds

# Maximum of number of data points per request
MAX_DPPR = 400 # data points (MAX_DPPR - Max data points per request) ( enabled chucked http request size ( default at 40960 ))
# 80 for config 4096

# Metric template
import random
def metric_template(running_timestamp):
    return {
        "metric": 'level',
        "timestamp": running_timestamp,
        "value": value_generator(4500, 5500),
        "tags": {'location':'yala'}
    }

def value_generator(start, end):
    return random.randint(start, end)
