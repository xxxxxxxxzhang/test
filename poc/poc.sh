#!/bin/bash
firefox --version
sleep 10
python3 /opt/poc/exp.py http://web 
echo "poc ok"