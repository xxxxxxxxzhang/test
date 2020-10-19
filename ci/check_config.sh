#!/bin/bash

config_result=`sudo docker-compose logs config`

echo "$config_result"

[[ $config_result =~ "Config Success!" ]] || exit -1