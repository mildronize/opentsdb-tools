#!/bin/bash

INPUT_DIR="/home/mildronize/external/thesis/generated-dps"
CONTAINER_NAME="opentsdb"
LOG_PATH="./logs"
# tsdb path in Docker
TSDB_CLI_PATH="./tsdb"
# start time when using `tsdb scan`
START_TIME="2000/01/01-00:00:00"

IMPORT_LOG_PATH="./import_log.csv"

mkdir -p $LOG_PATH


function tsdb_mkmetric {
    metric_name=$1
    docker exec -it $CONTAINER_NAME $TSDB_CLI_PATH mkmetric $metric_name
}

function tsdb_import {
    id=$1
    import_file=$2
    docker exec -it $CONTAINER_NAME $TSDB_CLI_PATH import ./generated-dps/$import_file 1> $LOG_PATH/$id.import 2> $LOG_PATH/$id.import.err
    cat $LOG_PATH/$id.import | awk '/tsd\./ {print}' > $LOG_PATH/$id.import.stat
}

# function tsdb_count {
    # Count DPS and errors
    # id=$1
    # nthread=$2
    # tsdb_counting $id $nthread
    # tsdb_count_dps $id $nthread
    # tsdb_count_errors $id
# }

# function tsdb_counting_tmp {
    # bash -c 'echo $RANDOM' | read ran; echo /tmp/opentsdb-$ran |
    # read filename; \
        # docker exec -it $CONTAINER_NAME $TSDB_CLI_PATH fsck --full-scan --threads=8 > $filename; \
        # echo $filename;
# }

function tsdb_counting {
    id=$1
    nthread=$2
    docker exec -it $CONTAINER_NAME $TSDB_CLI_PATH fsck --full-scan --threads=$nthread > $LOG_PATH/$id.fsck ;
}

function tsdb_count_dps_fsck {
    id=$1
    nthread=$2
    # echo "tsdb_count_dps_fsck $id $nthread"
    # cat $LOG_PATH/$id.fsck |
    # awk '/Valid Datapoints/ {print $8}'

    cat $LOG_PATH/$id.fsck |
    awk '/Valid Datapoints/ {print $8}' |
    tr -d '\r' |
    read num; echo "$num / $nthread" | bc
}

function tsdb_count_dps_scan {
    docker exec -it $CONTAINER_NAME $TSDB_CLI_PATH scan --import $START_TIME sum level |
    grep 'location=hatyai' | wc -l
}

function tsdb_count_errors {
    id=$1
    cat $LOG_PATH/$id.fsck |
    awk '/Total Errors:/ {print $8}' |
    tr -d '\r'
}

function tsdb_get_file_size {
    du -s $1 | awk '{print $1}'
}

function tsdb_run_test {
    id=$1
    nthread=$2

    input_file_path="$INPUT_DIR/dps-$id"
    hbase_storage_path="/home/mildronize/external/hbase"

    echo $id $nthread
    # tsdb_import $id dps-$id
    # tsdb_counting $id $nthread
    # total_dps_fsck=$( tsdb_count_dps_fsck $id $nthread )
    # total_dps_scan=$(tsdb_count_dps_scan)
    tsdb_import $id dps-$id
    tsdb_counting $id $nthread
    total_dps_fsck=$(tsdb_count_dps_fsck $id $nthread)
    # total_dps_scan=$(tsdb_count_dps_scan)
    total_dps_error=$(tsdb_count_errors $id)
    input_file_size=$(tsdb_get_file_size $input_file_path)
    hbase_storage_size=$(tsdb_get_file_size $hbase_storage_path)
    # write to csv
    echo $id,$total_dps_fsck,$total_dps_scan,$total_dps_error,$input_file_size, $hbase_storage_size >> $IMPORT_LOG_PATH
    # total_dps_fsck=$(tsdb_count_dps_fsck $id $nthread)
    # read num; printf "Total dps(fsck): %d dps\n" $num
    # read num; printf "Total dps(scan): %d dps\n" $num
    # read num; printf "Total Errors   : %d dps\n" $num
}


# function tsdb_start_import {
num=$1
nthread=$2
echo id,total_dps_fsck,total_dps_scan,total_dps_error,input_file_size,hbase_storage_size >> $IMPORT_LOG_PATH

id=1
while [ $id -le $num ]
do
    echo Task $id
    tsdb_run_test $id $nthread
    id=$((id+1))
done
# }

# for i in {1..50}
# do
# cat 11.fsck| awk '/Valid Datapoints/ {print $8}' | tr -d '\r' | read num; echo "$num / 8" | bc
# done
