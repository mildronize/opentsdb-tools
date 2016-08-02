# To measure stat of OpenTSDB query
import requests
import time
import logging
import collections
logging.basicConfig(level=logging.INFO)

#  from opentsdb_importer.utils import *
import opentsdb_importer.config as config


def submit_job(year_start, year_end, downsampling):
    url = "http://{}:{}/api/query?" \
        "start=20{:02d}/01/01-00:00:00&end=20{:02d}/01/01-00:00:00" \
        "&m=sum:{}:level&show_summary=true&show_query=true".format(config.SERVER_IP,
                                                                   config.SERVER_PORT,
                                                                   year_start,
                                                                   year_end,
                                                                   downsampling)
    logging.info("HTTP requesting.. " + url)
    r = requests.get(url)
    if r.status_code != requests.codes.ok:
        logging.error(r.text)
        exit(1)
    return r.json()

#  submit_job(1,2,"1y-avg")


def measure(year_start, year_end, downsampling):
    stat = {}
    #  current_stats_id = len(stats) - 1
    #  no_experimental = year
    start_time = time.time()
    response = submit_job(year_start, year_end, downsampling)[1]["statsSummary"]
    stat["overall_time"] = (time.time() - start_time) * 1000
    # measure with this program
    stat["start_time"] = start_time
    # global
    stat["processingPreWriteTime"] = \
        response["processingPreWriteTime"]
    stat["emittedDPs"] = response["emittedDPs"]
    # query queryIdx_00
    stat["aggregationTime"]  = \
        response["queryIdx_00"]["aggregationTime"]
    stat["serializationTime"] = \
        response["queryIdx_00"]["serializationTime"]
    stat["queryScanTime"] = \
        response["queryIdx_00"]["queryScanTime"]
    stat["uidToStringTime"] = \
        response["queryIdx_00"]["uidToStringTime"]
    # scanner scannerIdx_00
    stat["compactionTime"] = response["queryIdx_00"][
        "scannerStats"]["scannerIdx_00"]["compactionTime"]
    stat["hbaseTime"] = \
        response["queryIdx_00"]["scannerStats"]["scannerIdx_00"]["hbaseTime"]
    stat["scannerTime"] = \
        response["queryIdx_00"]["scannerStats"]["scannerIdx_00"]["scannerTime"]

    return stat


def print_to_csv(stat, output, has_header):
    ordered_stat = collections.OrderedDict(
        sorted(stat.items(), key=lambda t: t[0]))
    with open(output, 'a') as f:
        # write header
        if has_header:
            line_output_tmp = ''
            for key, value in ordered_stat.items():
                line_output_tmp += ',"' + str(key) + '"'
            f.write(line_output_tmp[1:] + '\n')
        # write data
        line_output_tmp = ''
        for key, value in ordered_stat.items():
            line_output_tmp += ',"' + str(value) + '"'
        f.write(line_output_tmp[1:] + '\n')


def start_experimental_increment(year_start, year_end, downsampling, output):
    for year in range(year_start, year_end + 1):
        stat = measure(0, year, downsampling)

        has_header = False
        if year_start == year:
            has_header = True
        print_to_csv(stat, output, has_header)


def start_experimental_repeat(
        year_start,
        year_end,
        downsampling,
        num_repeat,
        output):
    for i in range(num_repeat):
        stat = measure(year_start, year_end, downsampling)

        has_header = False
        if i == 0:
            has_header = True
        print_to_csv(stat, output, has_header)
