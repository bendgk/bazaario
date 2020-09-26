#!/bin/bash
kill $(ps | grep -i  python | awk '{print $1}')
python3 ticker.py &
python3 main.py &
