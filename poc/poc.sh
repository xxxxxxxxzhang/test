#!/bin/bash
python --version
pip3 install -i https://pypi.tuna.tsinghua.edu.cn/simple requests selenium lxml
tar -xvzf /opt/poc/geckodriver-v0.26.0-linux64.tar.gz
chmod +x geckodriver
cp geckodriver /usr/local/bin/
firefox --version
sleep 10
python3 /opt/poc/check.py http://web

echo "datafill script done. run exp..."

python3 /opt/poc/exp.py http://web 

echo "OK!!!"