import signal

# Register an handler for the timeout
def handler(signum, frame):
	print "Forever is over!"
	raise Exception ()
# This function *may* run for an indetermined time...
def loop_forever(k):
	import time
	for i in range(1,k):
		print i,"sec"
		time.sleep(1)
	print ("Finito !")
	signal.alarm(0)
# Register the signal function handler
signal.signal(signal.SIGALRM, handler)
ii=9
while 1 :
	signal.alarm(10)
	try:
		loop_forever(ii)
		ii=ii+1
	except KeyboardInterrupt :
		print ("Interrotto")
	except Exception, exc: 
		print exc
		ii=5
	finally:
		print ("Finale")
