#!/bin/bash

poc_result=`sudo docker-compose logs poc`

echo "$poc_result"
[[ $config_result =~ "Poc Success!" ]] || exit -1