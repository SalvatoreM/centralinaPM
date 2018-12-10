#!/bin/sh
name=$(cat /home/pi/alfetta/etc/alfetta.conf |grep nome |cut -d\= -f2)
mac=$(/sbin/ifconfig wlan0 |grep HWaddr |cut -d " " -f10)
#mac=$(cat /home/pi/alfetta/add.mac)
#mac1=$(ifconfig eth0 | grep -o -E '([[:xdigit:]]{1,2}:){5}[[:xdigit:]]{1,2}')
echo $name
echo $mac
echo $mac1
echo 'curl "http://centraline:centraline@94.177.187.133/vpnman/register.php?mac='$mac'&nome='$name'"'>> /home/pi/alfetta/sended
curl 'http://centraline:centraline@94.177.187.133/vpnman/register.php?mac='$mac'&nome='$name
