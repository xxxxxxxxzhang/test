#!/bin/bash
pip3 install -i https://pypi.tuna.tsinghua.edu.cn/simple requests lxml
STATUS=""
while [ "$STATUS" != "200" ]
do
    echo "waiting for blog initialization..."
    sleep 1
    STATUS=$(curl -sL -w "%{http_code}" http://web -o /dev/null)
done
python3 opt/data/filldata.py http://web 

echo "data fill ok"