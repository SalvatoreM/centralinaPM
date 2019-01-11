#! /bin/bash
pm=$1
m=$2
q=$3
if [ $pm = "PM2.5" ]; then
	sed  -i s/^k2=.*/k2=$m/ /home/pi/alfetta/etc/alfetta.conf
	sed  -i s/^q2=.*/q2=$q/ /home/pi/alfetta/etc/alfetta.conf
fi
if [ $pm = "PM10" ]; then
	sed  -i s/^k1=.*/k1=$m/ /home/pi/alfetta/etc/alfetta.conf
	sed  -i s/^q1=.*/q1=$q/ /home/pi/alfetta/etc/alfetta.conf
fi
pkill -SIGUSR1 centralina.py
