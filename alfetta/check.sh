#!/bin/sh
ps auxw | grep centralina | grep -v grep > /dev/null
if [ $? -eq 0 ]
then
         echo "centraline.py is RUNNING" 
         echo "centralina.py is RUNNING" >/var/www/html/alfetta/process.log
else
         echo "centralina.py is STOPPED"
         echo "centralina.py is STOPPED" >/var/www/html/alfetta/process.log

fi

