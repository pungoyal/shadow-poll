#! /bin/bash

sudo kill -9 `ps -ef | grep route | grep python | awk '{print $2}'`

