#!/bin/bash

config_result=`sudo docker-compose logs poc`


[[ $config_result =~ "Poc Success!" ]] || exit -1