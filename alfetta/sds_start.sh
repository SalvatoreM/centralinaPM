#!/bin/sh
ps auxw | grep sds011 | grep -v grep > /dev/null
if [ $? != 0 ]
then
         echo "Process Started" > /var/www/html/alfetta/result.log
         /home/pi/alfetta/sds011.py
else
         echo "Process alredy Started" > /var/www/html/alfetta/result.log

fi

