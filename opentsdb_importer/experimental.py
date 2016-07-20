# To measure stat of OpenTSDB query
import requests
import time

from opentsdb_importer.utils import *
import opentsdb_importer.config as config

def submit_job(year, downsampling):
    url = "http://"+config.SERVER_IP+":"+config.SERVER_PORT+"/api/query?start=2000/01/01-00:00:00&end=20%02d/01/01-00:00:00&m=sum:%s:level&show_summary=true&show_query=true" % (year, downsampling)
    print(url)
    # time.sleep(1)
    r = requests.get(url)
    if r.status_code != requests.codes.ok:
        print("Error! " + str(r.status_code))
        print(r.text)
        exit(1)
    return r.json()

def start_experimental(downsampling):
    stats = []
    for year in range(1,3):
        stats.append({})
        current_stats_id = len(stats) - 1
        no_experimental = year
        start_time = time.time()
        response = submit_job(year, downsampling)[1]["statsSummary"]
        stats[current_stats_id]["overall_time"] = time.time() - start_time
        # measure with this program
        stats[current_stats_id]["start_time"] = start_time
        # global
        stats[current_stats_id]["processingPreWriteTime"] = \
            response["processingPreWriteTime"]
        stats[current_stats_id]["emittedDPs"] = response["emittedDPs"]
        # query queryIdx_00
        stats[current_stats_id]["aggregationTime"]  = \
            response["queryIdx_00"]["aggregationTime"]
        stats[current_stats_id]["serializationTime"] = \
            response["queryIdx_00"]["serializationTime"]
        stats[current_stats_id]["queryScanTime"] = \
            response["queryIdx_00"]["queryScanTime"]
        stats[current_stats_id]["uidToStringTime"] = \
            response["queryIdx_00"]["uidToStringTime"]
        # scanner scannerIdx_00
        stats[current_stats_id]["compactionTime"] = \
            response["queryIdx_00"]["scannerStats"]["scannerIdx_00"]["compactionTime"]
        stats[current_stats_id]["hbaseTime"] = \
            response["queryIdx_00"]["scannerStats"]["scannerIdx_00"]["hbaseTime"]
        stats[current_stats_id]["scannerTime"] = \
            response["queryIdx_00"]["scannerStats"]["scannerIdx_00"]["scannerTime"]
    write_to_csv_file(stats)

def write_to_csv_file(stats):
    f = open('stats.csv', 'w')
    # write header
    line_output_tmp = 'No'
    for key, value in stats[0].items():
        line_output_tmp += ',"'+ str(key) + '"'
    f.write(line_output_tmp+'\n')
    # write data
    for no_experimental, stat in enumerate(stats, start = 1):
        line_output_tmp = str(no_experimental)
        for key, value in stat.items():
            line_output_tmp += ',"'+ str(value) + '"'
        f.write(line_output_tmp+'\n')
    pass

start_experimental(downsampling = "1y-avg")
