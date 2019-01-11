#!/bin/sh
r=$(grep -c PAUSE "/var/www/html/alfetta/sensor.log";)
echo $r
if [ $r != 0 ]
then
         echo "Process Stopped" > /var/www/html/alfetta/result.log
         pkill centralina.py
else
         echo "Process NOT IN PAUSE - Try again when in PAUSE" > /var/www/html/alfetta/result.log
fi

