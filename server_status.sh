#!/bin/bash
url=http://localhost:4242
sleep_time=1

echo Server Status \( $url \)

while true; do
    curl -s $url > /dev/null
    exit_code=$?
    if [ $exit_code -eq 0 ]; then
        echo -ne "${COLOR_GREEN}UP${COLOR_NC}             \r"
    else
        echo -ne "${COLOR_RED}DOWN${COLOR_NC}             \r"
    fi
    sleep $sleep_time
done
