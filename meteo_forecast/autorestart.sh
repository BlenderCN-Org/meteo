#!/bin/bash


# relance de meteo_download si ne tourne pas
running=$(ps -f -C python3|grep 'meteo_download.py'|wc -l)
echo "running = $running"
if [ $running -eq 1  ] ; then
    echo "`date` => meteo_download.py is running"
else
    if [ $running -eq 0 ] ; then
        echo "restarting meteo_download.py"
        cd meteo_download && python3 meteo_download.py
    fi
fi
