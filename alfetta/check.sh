#!/bin/sh
ps auxw | grep sds011 | grep -v grep > /dev/null
if [ $? -eq 0 ]
then
         echo "sds011.py is RUNNING" 
         echo "sds011.py is RUNNING" >/var/www/html/alfetta/process.log
else
         echo "sds011.py is STOPPED"
         echo "sds011.py is STOPPED" >/var/www/html/alfetta/process.log

fi

