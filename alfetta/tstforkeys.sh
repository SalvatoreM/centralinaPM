#! /bin/sh
name=$(cat /home/pi/alfetta/etc/alfetta.conf |grep nome |cut -d\= -f2)
echo $name
/usr/bin/wget http://94.177.187.133/centraline/$name.crt -O /etc/openvpn/aria.crt
if [ -s /etc/openvpn/aria.crt ]
then
	echo "scaricato $name.crt"
	/usr/bin/wget http://94.177.187.133/centraline/$name.key -O /etc/openvpn/aria.key
	if [ -s /etc/openvpn/aria.key ]
	then
		echo "scaricato $name.key" >>/home/pi/alfetta/sended
#
	   /usr/bin/wget http://94.177.187.133/centraline/$name.ta.key -O /etc/openvpn/ta.key
	   if [ -s /etc/openvpn/ta.key ]
		   echo "scaricato $name.ta.key" >>/home/pi/alfetta/sended
		   ( crontab -l | grep -v -F "tstforkeys.sh" ) | crontab -
		   echo "CronJob  tstforkeys.sh eliminato" >>/home/pi/alfetta/sended
        /usr/sbin/openvpn --config /etc/openvpn/client.conf
	   else
		   echo  "non scaricato $name.ta.key" >>/home/pi/alfetta/sended
	   fi
	else
		echo  "non scaricato $name.key" >>/home/pi/alfetta/sended
	fi
else
		echo " non scaricato $name.crt" >>/home/pi/alfetta/sended
fi
