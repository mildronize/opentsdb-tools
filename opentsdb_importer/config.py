SERVER_IP   = "172.30.235.80"
SERVER_PORT = "4242"

# "send_metrics" config for trying to resend(reflush) the data again
NUM_TRY                         = 5 # times
TIME_DELAY_BEFORE_TRY_NEW_FLUSH = 60 # seconds

# Maximum of number of data points per request
MAX_DPPR = 400 # data points (MAX_DPPR - Max data points per request) ( enabled chucked http request size ( default at 40960 ))
# 80 for config 4096
