#! /bin/bash
wpa_passphrase $1 $2 >/home/pi/alfetta/etc/wpa_supplicant.add
cat   /home/pi/alfetta/etc/wpa_supplicant.head > /home/pi/alfetta/etc/wpa_supplicant.conf
cat   /home/pi/alfetta/etc/wpa_supplicant.add >> /home/pi/alfetta/etc/wpa_supplicant.conf 
#rm  /home/pi/alfetta/etc/wpa_supplicant.add
cp   /home/pi/alfetta/etc/wpa_supplicant.conf  /etc/wpa_supplicant/wpa_supplicant.conf 
#rm /home/pi/alfetta/etc/wpa_supplicant.conf 
ifdown wlan0
sleep 2s
ifup wlan0
