#! /usr/bin/python
import signal
import os
import time

def receive_signal(signum, stack):
    print 'Received:', signum

signal.signal(signal.SIGUSR1, receive_signal)
signal.signal(signal.SIGUSR2, receive_signal)

print 'My PID is:', os.getpid()

while True:
   try:
    print 'Waiting...'
    time.sleep(3)
   except Exception, e:
    print ("aaaaaa")
