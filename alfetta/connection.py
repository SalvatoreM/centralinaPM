#!/usr/bin/python
#
#
import urllib2
import time

def internet_on():
    try:
        urllib2.urlopen('http://salvatorehost.no-ip.org/db/write', timeout=1)
        return True
    except urllib2.URLError as err: 
        return False



while True :
	print ("prova "+time.strftime("%H:%M:%S"))
	if (internet_on()):
		print ("provato OK "+time.strftime("%H:%M:%S"))
	else:
		print ("provato NOT OK "+time.strftime("%H:%M:%S"))
	time.sleep(5)

