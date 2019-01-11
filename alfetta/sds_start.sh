#!/bin/sh
ps auxw | grep centralina | grep -v grep > /dev/null
if [ $? != 0 ]
then
         echo "Process Started" > /var/www/html/alfetta/result.log
         /home/pi/alfetta/centralina.py
else
         echo "Process alredy Started" > /var/www/html/alfetta/result.log

fi

