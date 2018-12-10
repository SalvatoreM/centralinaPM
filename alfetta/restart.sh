#!/bin/sh
ps auxw | grep sds011 | grep -v grep > /dev/null
if [ $? -eq 0 ]
then 
r=$(grep -c PAUSE "/var/www/html/alfetta/sensor.log";)
echo "PAUSE = $r"
while [ $r -eq 0 ]; do
r=$(grep -c PAUSE "/var/www/html/alfetta/sensor.log";)
echo wait...$r
done
pkill sds011.py
sleep 1
ps auxw | grep sds011 | grep -v grep > /dev/null
if [ $? != 0 ]
then
echo Started!!!!
/home/pi/alfetta/sds011.py
fi
fi
