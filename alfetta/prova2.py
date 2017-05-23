import sys
import traceback
ii=1
try:
	ii=ii+1/0
except Exception, exc:
	exec_info= sys.exc_info()
	print exec_info[0]
	print exec_info[1]
	print exec_info[2]
	
	print traceback.print_exception(*exec_info)
finally:
	print ("Finale")

