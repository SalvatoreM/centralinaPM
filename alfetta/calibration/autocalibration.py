#! /usr/bin/python
import os
import sys
import string
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
def read_conf(filename):
    print ("Read_Conf\n")
    config={}
    config["host"]=[]
    in_file = open(filename,"r")
    while True:
        in_line = in_file.readline()
        if in_line == "":
            break
        in_line = in_line[:-1]
        [chiave,valore] = string.split(in_line,"=")
        if (chiave=="host"):
            config["host"].append(string.split(valore,","))
        else :
            config[chiave] = valore
    in_file.close()
    return (config)
#------------------------------------------------------------------------------
def calibration (pm,exc):
   esclude=eval(exc)
   N_DAY_MAX=30
#   a=os.popen("grep "+pm+" /home/pi/alfetta/calibration/datalog"+pm+".log").read().split("\n") # Strumento in calibrazione
#   ra=os.popen("grep "+pm+" /home/pi/alfetta/calibration/reference"+pm+".log").read().split("\n")  # Strumento Campione
   a=os.popen("grep -E '"+pm+"[ ]{1,2}\|"+"' /home/pi/alfetta/calibration/datalog"+pm+".log").read().split("\n") # Strumento in calibrazione
   ra=os.popen("grep -E '"+pm+"[ ]{1,2}\|"+"' /home/pi/alfetta/calibration/reference"+pm+".log").read().split("\n")  # Strumento Campione
#   b=[0]*N_DAY_MAX    # Valori non calibrati
   b=[0]    # Valori non calibrati
   rb=[0]   # Valori di Riferimento
   h=0
   count=0
   offset=0
   # estrazione valori dal file locale delle medie orarie
   for x in a :
      print x
      if len(x) > 20  :
         h1=int(x.split("|")[0].split(":")[0])
         if (h != h1):
            b[h+offset]=b[h+offset]/count
            if h1 < h :
               offset=offset+24
               b.append(0)
               print offset
            else :               
               for e in range(0,(h1-h)):
                  b.append(0)
            count = 0
            h=h1
#         b[int(x.split("|")[0].split(":")[0])+offset]+=float(x.split("|")[1])
         b[h1+offset] += float(x.split("|")[1])
         count = count+1
#   if (count < 24):
#      print count
#      exit(1)
   print ("Dimensione di b ",h1+offset,count)
   b[h1+offset]=b[h1+offset]/count
   count=0
   offset=0
   h=0
   # estrazione valori Campione dal file delle medie orarie
   for x in ra :
#      print x
      if len(x)> 20  :
         h1=int(x.split("|")[0].split(":")[0])
         if (h != h1):
            rb[h+offset]=rb[h+offset]/count
            if (h1 < h) :
               offset=offset+24
               rb.append(0)
            else :
               for e in range(0,(h1-h)):
                  rb.append(0)
            count = 0
            h=h1
         rb[h1+offset]+=float(x.split("|")[1])
         count=count+1
#   if (count <24):
#      print count
#      exit(1)
#   count=0  
#   h=0
   print ("Dimensione di rb ",h1+offset,count)
   rb[h1+offset]=rb[h1+offset]/count
   m=0
   xmedio=0
   ymedio=0
   sq=0
   # Calcolo Valori della retta di Regressione Lineare 1^ grado
   print "["
   max_x=-10000
   min_x=1000
   distribution_file=open("/var/www/html/alfetta/distribution","w")
   print "["
   distribution_file.write( "[")
   count=0
   for i,x in enumerate(b):
#      print "index = ",i,len(rb),len(b),"\n";
      if i < len(rb) :
	radius=1
	print i, (i in esclude)
      	if (x >0 and rb[i] >0 and (not(i in esclude))):
	   radius=3
           xmedio=xmedio+x
           ymedio=ymedio+rb[i]
           count=count+1
           if x < min_x :
              min_x =x
           if x > max_x:
              max_x =x
#           xmedio=xmedio/count 
#           ymedio=ymedio/count
#   for i,x in enumerate(b):
#      xmedio=xmedio+x/len(b)
#      ymedio=ymedio+rb[i]/len(b)
#      if x < min_x :
#         min_x =x
#      if x > max_x:
#         max_x =x
      # x Strumento  in calibrazione y Strumento Campione
#      print " Media "+pm+" alle ore {:2d} --> x={:5.2f} y={:5.2f}".format(i,x,rb[i])
        if (i>0):
      	  print ",{"+"x:{:5.2f},y:{:5.2f},r:{}".format(x,rb[i],radius)+"}"
          distribution_file.write( ",{"+"x:{:5.2f},y:{:5.2f},r:{}".format(x,rb[i],radius)+"}")
        else:
      	  print "{"+"x:{:5.2f},y:{:5.2f}".format(x,rb[i])+"}"
          distribution_file.write("{"+"x:{:5.2f},y:{:5.2f},r:{}".format(x,rb[i],radius)+"}")
   print "]"
   distribution_file.write( "]")
   distribution_file.close()
   if (mod_zerointercetta == "0"):
      xmedio=xmedio/count 
      ymedio=ymedio/count
   else : 
      xmedio = 0
      ymedio = 0
   for i,x in enumerate (b):
      if i < len(rb)and (not(i in esclude)) :
          m=m+((x-xmedio)*(rb[i]-ymedio))  # Pendenza
          sq=sq+(x-xmedio)*(x-xmedio)      
   m=m/sq
   q=ymedio-m*xmedio                       # Intercetta
   if q >= 0 :
      print pm+": equazione = {:.2f}x+{:.2f}".format(m,q)
   if q < 0  :
      print pm+": equazione = {:.2f}x{:.2f}".format(m,q)
# Calcolo del coefficiente di determinazione
   dev_reg=0
   dev_e=0
   for i,y in enumerate(rb):
      if (i < len(b) and ( not(i in esclude))):
          dev_reg=dev_reg+((m*b[i]+q)-ymedio)**2
          dev_e=dev_e+(y-(m*b[i]+q))**2
   r2=1-(dev_e/(dev_e+dev_reg))
   print " R2 = {:5.2}".format(r2)
   return (m,q,r2,min_x,max_x)
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
#--------- Main ---------------------------------------------------------------------
try:
   print sys.argv[1]
   if (sys.argv[1] != "PM10") and (sys.argv[1] != "PM2.5"):
      print "Parametro Sconosciuto\n"
      exit (1)
   pm=sys.argv[1]
   if len (sys.argv) > 2:
      exclusion=sys.argv[2]
      print exclusion
      mod_zerointercetta=sys.argv[3]
   else :
      mod_zerointercetta = "0"
      exclusion='[]'

   configurazione=read_conf("/home/pi/alfetta/etc/alfetta.conf")
   m,q,r2,min_b,max_b=calibration (pm,exclusion)
   regression_file=open("/var/www/html/alfetta/regressione","w")
   coefficient_file=open("/var/www/html/alfetta/coefficient","w")
   print m,q,r2   
   coefficient_file.write( '{'+'"m":"{:.2f}","q":"{:.2f}","r2":"{:.2f}"'.format(m,q,r2)+'}')
   coefficient_file.close()
   print "{"+"x:{:.2f},y:{:.2f}".format(min_b,m*min_b+q)+"},"
   print "{"+"x:{:.2f},y:{:.2f}".format(max_b,m*max_b+q)+"}"
   regression_file.write("{"+"x:{:.2f},y:{:.2f}".format(min_b,m*min_b+q)+"},")
   regression_file.write("{"+"x:{:.2f},y:{:.2f}".format(max_b,m*max_b+q)+"}")
   regression_file.close()
   if (r2 > 0.9):
      if pm == "PM2.5":
         new_m=m*float(configurazione["k2"])
         new_q=m*float(configurazione["q2"])+q
         comand ="sed  -i s/^k2=.*/k2="+"{:.3f}".format(new_m)+"/ /home/pi/alfetta/etc/alfetta.conf"
         print comand
#      os.system(comand)
         comand ="sed  -i s/^q2=.*/q2="+"{:.3f}".format(new_q)+"/ /home/pi/alfetta/etc/alfetta.conf"  
         print comand
#     os.system(comand)
      elif pm == "PM10" :
         new_m=m*float(configurazione["k1"])
         new_q=m*float(configurazione["q1"])+q
         comand ="sed  -i s/^k1=.*/k1="+"{:.3f}".format(new_m)+"/ /home/pi/alfetta/etc/alfetta.conf"
         print comand
#      os.system(comand)
         comand ="sed  -i s/^q1=.*/q1="+"{:.3f}".format(new_q)+"/ /home/pi/alfetta/etc/alfetta.conf"
         print comand
#      os.system(comand)
   exit(0)
except Exception as e:
   f=open("/home/pi/alfetta/calibration/autocalibration.log","a")
   f.write(str(e)+"\n");
   f.close()
#   print str(e)
   exit(1)



