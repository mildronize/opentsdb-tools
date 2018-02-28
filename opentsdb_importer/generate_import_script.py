import os

def get_bash_sleep_counter():
    return """
function sleep_counter {
    time=$1
    time=$((time-1))
    echo "Sleeping for $time seconds"
    for i in $(seq $time -1 0)
    do
        # echo $i
        echo -ne 'Remaining time: '
        if [ $i -lt 60 ]; then
            echo -ne "$i seconds\\r"
        else
            minute=$((i/60))
            echo -ne "$minute minutes\\r"
        fi

        sleep 1
    done
    echo -ne 'Finished                  \\r'
    echo -ne '\\n'
}
"""

def generate_import_string(num_files, sleep, chunk_size, tsdb_path ,prefix = "dps-"):
    prefix = prefix
    result = ""
    result += "#!/bin/bash" + os.linesep
    result += get_bash_sleep_counter()  + os.linesep
    is_last_loop = False
    for i in range(1,num_files+1, chunk_size):
        result += "{} import".format(tsdb_path)
        if num_files % chunk_size != 0 and i + chunk_size > num_files:
            actual_chunk_size = num_files % chunk_size
            is_last_loop = True
        else:
            actual_chunk_size = chunk_size
        target_files = ""
        for chunk_id in range(actual_chunk_size):
            target_files += " %s%d" % (prefix, chunk_id + i)
        result += target_files
        if not is_last_loop :
            result += os.linesep + "clear" + os.linesep
            result += "echo Finished importing {}{}".format(target_files, os.linesep)
            result += "sleep_counter %d" % sleep + os.linesep
    return result

