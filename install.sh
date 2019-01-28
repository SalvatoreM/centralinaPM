#!/bin/bash
# Ref to howners change howner and permission  files
# Copy files to OS filesystem
# update crontab file for  root
# update incrotab file for root
# assigne sudo privileges to www-data  to esecute as root iw iwlist
# 
#-------------------------------------------------------
./preinstall.sh
cat howners | \
while read CMD; do
    if [[ "$CMD" == *: ]]
    then
      echo Directory $CMD
      path=$(echo $CMD | sed -r 's/[:]/\//g')
      echo "path=$path"
    else
      if [[ "$CMD" == [-d]* ]]
      then 
          a=$(echo $CMD |cut -d' ' -f3)
          b=$(echo $CMD |cut -d' ' -f4)
          c=$(echo $CMD |cut -d' ' -f9)
          echo 'chown' $a:$b $path$c
          chown $a:$b $path$c
      fi
#     echo $CMD
    fi
#    echo $CMD
#    echo $CMD |cut -d' ' -f1 | $CMD
done
#-------------------------------------------------------
cp -pr alfetta/.  /home/pi/alfetta/
cp -pr html/. /var/www/html/
cp -pr usr/bin/autohotspot  /usr/bin
cp -pr etc/openvpn/client.conf  /etc/openvpn/
cp -pr etc/openvpn/ca.crt  /etc/openvpn/
cp -pr etc/dnsmasq.conf  /etc/dnsmasq.conf
cp -pr etc/hostapd/hostapd.conf  /etc/hostapd/hostapd.conf
cp -pr etc/systemd/system/autohotspot.service /etc/systemd/system/autohotspot.service
#-------------------------------------------------------------------------------------
systemctl enable autohotspot.service
#-------------------------------------------------------
FILE=/var/spool/incron/root
touch  $FILE
chmod 600 $FILE
cat var/spool/incron/root | \
while read LINE; do
        grep -qF -- "$LINE" "$FILE" || echo "$LINE" >> "$FILE"
done
#-------------------------------------------------------
FILE=/var/spool/cron/crontabs/root
touch  $FILE
chmod 600 $FILE
cat var/spool/cron/crontabs/root | \
while read LINE; do
        grep -qF -- "$LINE" "$FILE" || echo "$LINE" >> "$FILE"
done
#-------------------------------------------------------
if ! grep 'www-data ALL=NOPASSWD: /sbin/iwlist , /sbin/wpa_cli' /etc/sudoers; then
	sed -i  '/root.*ALL=(ALL:ALL) ALL/a www-data ALL=NOPASSWD: /sbin/iwlist , /sbin\/wpa_cli'  /etc/sudoers
fi
#-------------------------------------------------------


