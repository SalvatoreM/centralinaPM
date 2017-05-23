#!/usr/bin/python
#coding=utf-8
#============================================================================
#============================================================================
#============================================================================
#============================================================================
#============================================================================
#============================================================================
from __future__ import print_function
import serial, struct, sys, time
import string
import threading
import os
import datetime
import smtplib
import base64
import urllib2
import signal
#============================================================================
#============================================================================
class logger():
	def __init__(self,logfile,name):
#		print ("init Logger")
		self.reg=False
		self.report=False
		self.name=""
		self.path=""
		self.records=[]
		self.IDname=name
		self.h=time.strftime("%H")
		self.pm10maxt=time.strftime("%H:%M")
		self.pm25maxt=time.strftime("%H:%M")
		self.pm10_y=0
		self.pm25_y=0
		self.pm10_year=0
		self.pm25_year=0
		self.n_day=0
		self.pm25_over_OMS=0
		self.pm10_over_OMS=0
		self.pm25_over=0
		self.pm10_over=0
		filename=string.split(logfile,"/")
		for f in filename[:-1]:
			self.path=self.path+f+"/"
		for f in filename[-1:]:
			self.name=self.name+f
#		print self.path+self.name
		if (not os.path.isfile(self.path+self.name)):
			dfile = open (self.path+self.name,"w")
			dfile.write ("Nuovo File del "+time.strftime("%c")+"\n")
			dfile.close
#		print ("logger installed")
#============================================================================
#============================================================================
	def event_log(self,message):
#		print time.strftime("%H:%M")
#		print self.path+self.name
		dfile = open (self.path+self.name,"a")
#		print message
		dfile.write (message)
		dfile.close()
		self.archive()
#============================================================================
#============================================================================
	def archive(self):
		if (time.strftime("%H:%M") >= "00:00" and time.strftime("%H:%M") <"00:30"):
#		if (time.strftime("%H:%M") == "00:07"):
			if (not self.reg):
				self.reg=True
				os.system ("mv "+self.path+self.name+" "+self.path+time.strftime("%a-%d-%b-%Y_")+self.name)
				self.send_report()
		elif (time.strftime("%H:%M") > "00:30"):
			if (self.reg):
				self.reg=False
				self.report=False

#============================================================================
#============================================================================
	def send_report(self):
		if (time.strftime("%H:%M") >= "00:00" and time.strftime("%H:%M") <"00:30"):
#		if (time.strftime("%H:%M") >= "00:00" and time.strftime("%H:%M") <"23:30"):
			if (not self.report):
				f=open("/home/pi/alfetta/etc/mail_account","r")
				self.account=string.split(f.read(),"\n")
				f.close()
                	if (string.split(self.account[0],"#")[1]  == "yes"):
				print (self.account)
    				self.user=string.split(self.account[2],"#")[1]
    				self.passw=string.split(self.account[3],"#")[1]
    				self.sender=string.split(self.account[4],"#")[1]
    				self.receiver=string.split(self.account[5],"#")[1]
	    			self.provider=string.split(self.account[1],"#")[1]
	    			self.testo="Buongiorno  da "+self.IDname+",\n  questa è l'aria che hai respirato ieri \n\n"
	    			self.testo=self.testo+"Valore medio Giornaliero                    PM10  = "+"%3.0f"%(self.pm10_day)+" ug/m3\n"
	    			self.testo=self.testo+"Valore Max medio Orario                     PM10  = "+"%3.0f"%(self.pm10max)+" ug/m3"+"alle "+self.pm10maxt+"\n"
	    			self.testo=self.testo+"Valore Min medio Orario                     PM10  = "+"%3.0f"%(self.pm10min)+" ug/m3\n"
	    			self.testo=self.testo+"Valore Inizio rilevamento (%3d  giorni)     PM10  = "%(self.n_day)+"%3.0f"%(self.pm10_y)+" ug/m3\n"
		    		self.testo=self.testo+"Numero Giorni superato limite di legge      PM10  = "+"%3.0f"%(self.pm10_over)+"\n"
		    		self.testo=self.testo+"Numero Giorni superato limite  OMS          PM10  = "+"%3.0f"%(self.pm10_over_OMS)+"\n\n\n"
	    			self.testo=self.testo+"Valore medio Giornaliero                    PM2.5 = "+"%3.0f"%(self.pm25_day)+" ug/m3\n"
	    			self.testo=self.testo+"Valore Max medio Orario                     PM2.5 = "+"%3.0f"%(self.pm25max)+" ug/m3"+"alle "+self.pm25maxt+"\n"
		    		self.testo=self.testo+"Valore Min medio Orario                     PM2.5 = "+"%3.0f"%(self.pm25min)+" ug/m3\n"
	    			self.testo=self.testo+"Valore Inizio rilevamento (%3d  giorni)     PM25  = "%(self.n_day)+"%3.0f"%(self.pm25_y)+" ug/m3\n"
		    		self.testo=self.testo+"Numero Giorni superato limite di legge      PM25  = "+"%3.0f"%(self.pm25_over)+"\n"
	    			self.testo=self.testo+"Numero Giorni superato limite  OMS          PM25  = "+"%3.0f"%(self.pm25_over_OMS)+"\n\n\n"
#	    			self.testo=self.testo+"                               Centralina Lippi2\n"
		    		self.server=smtplib.SMTP(self.provider)
		    		self.server.login(self.user,base64.b64decode(self.passw))
	    			self.oggetto="Report Centralina Qualità dell'aria"
	    			self.messaggio="From:%s\nTo:%s\nSubject:%s\n\n%s" %(self.sender,self.receiver,self.oggetto,self.testo)
	    			self.server.sendmail(self.sender,self.receiver,self.messaggio)
	    			self.server.quit()
	    			self.event_log ("["+time.strftime("%c")+"] "+ "Report del giorno "+time.strftime("%A %B %d %Y")+" --"+ " INVIATO a "+self.receiver+"\n")
	    		self.report=True
	    		self.records=[]
	   		self.reset_report()
		elif (time.strftime("%H:%M") > "00:30"):
			if (self.report):
				self.report=False
#============================================================================
#============================================================================
	def eval_report(self,pm10,pm25):
# statistiche giornaliere PM10
		self.n=self.n+1
#  media su base minuto 
#-------------------------------------------------------------------------------
		if (self.n > 1 ):
			self.pm10_medio=(self.pm10_medio*(self.n-1)+pm10)/self.n
			self.pm25_medio=(self.pm25_medio*(self.n-1)+pm25)/self.n
		else :
			self.pm10_medio=pm10
			self.pm25_medio=pm25
#--------------------------------- Medie Orarie ----------------------------------------------
		if (self.h != time.strftime("%H") ):
			self.h=time.strftime("%H")
			self.pm10_h=self.pm10_medio
			self.pm25_h=self.pm25_medio
			self.n_h=self.n  # numero di campioni in un ora
#			self.pm10_medio=0
#			self.pm25_medio=0
			self.n=0
#--------------------------------Verifica Massimo e Minimo Orario -----------------
			if (self.pm10_h > self.pm10max):
				self.pm10max=self.pm10_h
            			self.pm10maxt=time.strftime("%H:%M")
			if (self.pm10_h < self.pm10min):
				self.pm10min=self.pm10_h
			if (self.pm25_h > self.pm25max ):
				self.pm25max=self.pm25_h
            			self.p25maxt=time.strftime("%H:%M")
			if (self.pm25_h < self.pm25min):
				self.pm25min=self.pm25_h
#--------------------------------- Medie Giornaliere ----------------------------------------------
			self.n_ore=self.n_ore+1
			if (self.n_ore > 1 ):
				self.pm10_day=(self.pm10_day*(self.n_ore-1)+self.pm10_h)/self.n_ore
				self.pm25_day=(self.pm25_day*(self.n_ore-1)+self.pm25_h)/self.n_ore
			else :
				self.pm10_day=self.pm10_h
				self.pm25_day=self.pm25_h
#--------------------------------- Media Annuale ----------------------------------------------
			if (time.strftime("%H") == "00"):
				self.n_day=self.n_day+1
				if (self.n_day > 1 ):
					self.pm10_y=(self.pm10_y*(self.n_day-1)+self.pm10_day)/self.n_day
					self.pm25_y=(self.pm25_y*(self.n_day-1)+self.pm25_day)/self.n_day
				else :
					self.pm10_y=self.pm10_day
					self.pm25_y=self.pm25_day
#------------------------------------------Fine Anno-------------------------------------------------
#--------------------------------Verifica e conteggio sforamenti -----------------
				if  (self.pm10_day > 50):
					self.pm10_over=self.pm10_over+1
				if  (self.pm10_day > 20):
					self.pm10_over_OMS=self.pm10_over_OMS+1
				if  (self.pm25_day > 25):
					self.pm25_over=self.pm25_over+1
				if  (self.pm25_day > 10):
					self.pm25_over_OMS=self.pm25_over_OMS+1
				if (time.strftime("%d%m") =="0101") :
					self_pm10_year=self.pm10_y
					self.pm25_year=self.pm25_y
					self.n_day=0
			self.save_report()
#-------------------------------------------------------------------------------
		retpm10=" PM10  |"
		retpm10=retpm10+(" % 3.2f"%(pm10)).center(8)
		retpm10=retpm10+"|"+(" % 3.2f"%(self.pm10_medio)).center(8)
		retpm10=retpm10+"|"+(" % 3.2f"%(self.pm10max)).center(8)
		retpm10=retpm10+"|"+(" % 3.2f"%(self.pm10min)).center(8)+"|"
#		retpm10=retpm10+"|"+(" % 3.2f"%(self.pm10_over)).center(8)
#		retpm10=retpm10+"|"+(" % 3.2f"%(self.pm10_over_OMS)).center(8)+"|"
# statistiche  PM2.5
#		retpm25="PM2.5 | % 3.2f | % 3.2f | % 3.2f | % 3.2f | % 3.2f |"%(pm25,self.pm25_medio,self.pm25max,self.pm25min,self.pm25_over)
		retpm25=" PM2.5 |"
		retpm25=retpm25+(" % 3.2f"%(pm25)).center(8)
		retpm25=retpm25+"|"+(" % 3.2f"%(self.pm25_medio)).center(8)
		retpm25=retpm25+"|"+(" % 3.2f"%(self.pm25max)).center(8)
		retpm25=retpm25+"|"+(" % 3.2f"%(self.pm25min)).center(8)+"|"
#		retpm25=retpm25+"|"+(" % 3.2f"%(self.pm25_over)).center(8)
#		retpm25=retpm25+"|"+(" % 3.2f"%(self.pm25_over_OMS)).center(8)+"|"
		return(retpm10,retpm25)
#============================================================================
#============================================================================
	def reset_report (self):
		self.n=0
		self.n_ore=0
		self.pm10_day=0
#		self.pm10_medio=0
		self.pm10_h=0
		self.pm10max=0
		self.pm10min=2000
		if (time.strftime("%d%m") =="0101"):
			self.pm10_over=0
			self.pm10_over_OMS=0
#		self.pm25_medio=0
		self.pm25_day=0
		self.pm25_h=0
		self.pm25max=0
		self.pm25min=2000
		if (time.strftime("%d%m") =="0101"):
			self.pm25_over=0
			self.pm25_over_OMS=0
#		self.legge_pm10=False
#		self.legge_pm25=False
#		self.OMS_pm10=False
#		self.OMS_pm25=False
#---------------------------------------------------------------------------------
	def save_report(self):
		f=open("/home/pi/alfetta/etc/report.save","w")
		f.write("self.n_ore="+"%3.2f\n"%(self.n_ore))
		f.write("self.n_day="+"%3.2f\n"%(self.n_day))
		f.write("self.pm10_day="+"%3.2f\n"%(self.pm10_day))
		f.write("self.pm25_day="+"%3.2f\n"%(self.pm25_day))
		f.write("self.pm10max="+"%3.2f\n"%(self.pm10max))					
		f.write("self.pm10min="+"%3.2f\n"%(self.pm10min))					
		f.write("self.pm25max="+"%3.2f\n"%(self.pm25max))					
		f.write("self.pm25min="+"%3.2f\n"%(self.pm25min))					
		f.write("self.pm10maxt="+"'%s'\n"%(self.pm10maxt))					
#		f.write("self.pm10mint="+"%s"%(self.pm10mint))					
		f.write("self.pm25maxt="+"'%s'\n"%(self.pm25maxt))					
#		f.write("self.pm25mint="+"%s"%(self.pm25mint))					
		f.write("self.pm10_y="+"%3.2f\n"%(self.pm10_y))				
		f.write("self.pm25_y="+"%3.2f\n"%(self.pm25_y))
		f.write("self.pm10_year="+"%3.2f\n"%(self.pm10_year))					
		f.write("self.pm25_year="+"%3.2f\n"%(self.pm25_year))
		f.write("self.pm25_over="+"%3.2f\n"%(self.pm25_over))					
		f.write("self.pm25_over_OMS="+"%3.2f\n"%(self.pm25_over_OMS))					
		f.write("self.pm10_over="+"%3.2f\n"%(self.pm10_over))					
		f.write("self.pm10_over_OMS="+"%3.2f\n"%(self.pm10_over_OMS))					
		f.close()
#---------------------------------------------------------------------------------
#---------------------------------------------------------------------------------
	def recover_report(self):
    		in_file = open("/home/pi/alfetta/etc/report.save","r")
    		while True:
        		in_line = in_file.readline()
        		if in_line == "":
            			break
        		in_line = in_line[:-1]
        		exec(in_line)
    		in_file.close()

#============================================================================
#---------------------------------------------------------------------------------
class sds011_sensor():

# "DATASHEET": http://cl.ly/ekot
 
    DEBUG = 0
    CMD_MODE = 2
    CMD_QUERY_DATA = 4
    CMD_DEVICE_ID = 5
    CMD_SLEEP = 6
    CMD_FIRMWARE = 7
    CMD_WORKING_PERIOD = 8
    MODE_ACTIVE = 0
    MODE_QUERY = 1
    
    def __init__ (self,dev):

#	print ("sensor SDs011 init")
        self.ser = serial.Serial()
        self.ser.port = dev
        self.ser.baudrate = 9600
        self.ser.open()
        self.ser.flushInput()
        self.byte, data = 0, ""
        self.pm10k=1
        self.pm10q=0
        self.pm25k=1
        self.pm25q=0
	self.pm10_acc=0
	self.pm25_acc=0
	self.pm10_act=0
	self.pm25_act=0
#la somma dei due paratri seguenti deve essere sempre = 6
	self.runtime=5    # 1-6 minuti   (1 2 3 4 5)
	self.sleeptime=1    # 0-5 minuti   (4 3 2 1 0)
#-----------------------------------------------------------
        self.samples=60          	# Numero di campioni per media default
#        self.Ton= 1       	       	#secondo default
        self.Toff=self.sleeptime * 60         		# tempo di pausa Laser OFF Ventola OFF default
        self.sync=0
        self_pm10_acc=0
        self.pm25_acc=0
	self.sample_number=0
#	print ("Cilco abilitato")
        self.sensor_on=threading.Thread(target=self.__ciclo)
	self.lock=threading.Lock()
	self.sensor_on.start()
	self.status="PAUSE"
#	print ("Init End")

    def get_status(self):
	return(self.status)

    def set_pm10_calibration (self,k,q):
        self.pm10k=k
        self.pm10q=q

    def set_pm25_calibration (self,k,q):
        self.pm25k=k
        self.pm25q=q

    def set_cicletime(self,runtime):
 	if runtime > 5 :
		runtime=5
	if runtime < 1 :
		runtime=1
#-----------------------------------------------------------
#la somma dei due parametri seguenti deve essere sempre = 6
#-----------------------------------------------------------
        self.runtime=runtime            # 1-6 minuti   (1 2 3 4 5) tempo di acquisione misure
	self.sleeptime=(5 - self.runtime)    # 0-5 minuti   (4 3 2 1 0) tempo di pausa (Laser OFF Fan OFF)
#-----------------------------------------------------------
        self.samples=60             	     # Numero di campioni per media default
        self.Toff=self.sleeptime * 60        # tempo di pausa Laser OFF Ventola OFF default

    def get_runtime(self):
	return(self.runtime)

    def get_sleeptime(self):
	return(5-self.runtime)

    def switch_on(self):
 	cmd_setsleep(0)
	time.sleep(3)

    def switch_off(self):
 	cmd_setsleep(1)
	time.sleep(3)

    def dump(self,d, prefix=''):
        print(prefix + ' '.join(x.encode('hex') for x in d))
 
    def construct_command(self,cmd, data=[]):
        assert len(data) <= 12
        data += [0,]*(12-len(data))
        checksum = (sum(data)+cmd-2)%256
        ret = "\xaa\xb4" + chr(cmd)
        ret += ''.join(chr(x) for x in data)
        ret += "\xff\xff" + chr(checksum) + "\xab"
        if self.DEBUG:
            self.dump(ret, 'Tx: ')
        return ret
 
    def process_data(self,d):
        r = struct.unpack('<HHxxBB', d[2:])
        self.pm25 = r[0]/10.0
        self.pm10 = r[1]/10.0
        checksum = sum(ord(v) for v in d[2:8])%256
#        print("PM 2.5: {} u/m^3  PM 10: {} u/m^3 CRC={}\n".format(self.pm25, self.pm10, "OK" if (checksum==r[2] and r[3]==0xab) else "NOK"))
        
    def process_version(self,d):
        r = struct.unpack('<BBBHBB', d[3:])
        checksum = sum(ord(v) for v in d[2:8])%256
#        print("Y: {}, M: {}, D: {}, ID: {}, CRC={}".format(r[0], r[1], r[2], hex(r[3]), "OK" if (checksum==r[4] and r[5]==0xab) else "NOK"))
 
    def read_response(self):
        byte = 0
        while byte != "\xaa":
            byte = self.ser.read(size=1)
        d = self.ser.read(size=9)
        if self.DEBUG:
            self.dump(d, 'Rx: ')
        return byte + d
 
    def cmd_set_mode(self,mode=MODE_QUERY):
        self.ser.write(self.construct_command(self.CMD_MODE, [0x1, mode]))
        self.read_response()
 
    def cmd_query_data(self):
        self.ser.write(self.construct_command(self.CMD_QUERY_DATA))
        d = self.read_response()
#       print (d[1].encode("hex"),"\xc0".encode("hex"))
        if d[1].encode("hex") == "\xc0".encode("hex"):
#            print ("process data: campione No. ",self.sample_number)
            self.process_data(d)
	else:
#		print ("Data Not OK")
		self.pm10=0
		self.pm25=0
 
    def cmd_set_sleep(self,sleep=1):
        mode = 0 if sleep else 1
        self.ser.write(self.construct_command(self.CMD_SLEEP, [0x1, mode]))
        self.read_response()
 
    def cmd_set_working_period(self,period):
        self.ser.write(self.construct_command(self.CMD_WORKING_PERIOD, [0x1, period]))
        self.read_response()
 
    def cmd_firmware_ver(self):
        self.ser.write(self.construct_command(self.CMD_FIRMWARE))
        d = self.read_response()
        self.process_version(d)
 
    def cmd_set_id(self,id):
        id_h = (id>>8) % 256
        id_l = id % 256
        self.ser.write(self.construct_command(self.CMD_DEVICE_ID, [0]*10+[id_l, id_h]))
        self.read_response()
 
    def set_pm10_calib(self,k,q):
        self.pm10k=k
        self.pm10q=q
            
    def set_pm25_calib(self,k,q):
        self.pm25k=k
        self.pm25q=q
            
    def elaborate (self):
        self.pm10_acc=self.pm10_acc+(self.pm10k*self.pm10+self.pm10q)/self.samples
        self.pm25_acc=self.pm25_acc+(self.pm25k*self.pm25+self.pm25q)/self.samples

    def measure(self,op):
	try:
		self.lock.acquire()
		if op=="update" :
			self.update_measure()
		if  op =="get":
			return(self.get_measure())
	finally:
		self.lock.release()
 
    def update_measure(self):
       	self.pm10_act = self.pm10_acc
       	self.pm25_act = self.pm25_acc
	self.validate=True
	print (self.pm10_act,self.pm25_act)
	self.pm10_acc=0
        self.pm25_acc=0  
        
    def get_measure(self):
#	try:
#       	self.lock.acquire()
#	print("GET MEASURE",self.sample_number)
	pm10_tmp=self.pm10_act
      	pm25_tmp=self.pm25_act
       	return (pm10_tmp,pm25_tmp,self.validate)

    def stop_ciclo(self):
	self.sensor_on.do_run=False
	self.sensor_on.join()
	return(True)
            
    def __ciclo(self):
#	print ("Partito !!!!")
	self.validate = False
#        self.cmd_set_sleep(1)
        self.cmd_set_mode(1);
#        self.cmd_firmware_ver()
        time.sleep(3)
	t=threading.currentThread()
        while getattr(t,"do_run",True):
	        Ton=self.runtime
		Toff=self.sleeptime*60
		Tmedia=self.samples
            	if (Toff > 30 ):
			print (time.strftime("%H:%M:%S"),"PAUSE",sensor.get_sleeptime())
			self.status="PAUSE"
			self.cmd_set_sleep(1)
			time.sleep(Toff-30)
			self.status="PRE RUNNING"
			print(time.strftime("%H:%M:%S"),"PRE RUNNING")
			self.cmd_set_sleep(0)
	               	time.sleep(30) 		# accenzione 
		print (time.strftime("%H:%M:%S"),"RUNNING", sensor.get_runtime())
		self.status="RUNNING"
		for j in range(1,Ton+1):
	            	for i in range (1,Tmedia+1):
				inizio=time.time()
#               	    	self.cmd_set_mode(1);
                   		self.cmd_query_data();
                    		self.elaborate()             # esegue per ora solo la media 
#                   		self.cmd_set_mode(0);
				self.sample_number=i
				fine=time.time()
#				print ("Durata", fine-inizio)
                    		time.sleep(1)
     			self.measure("update")
	self.cmd_set_sleep(1)
        print ("STOP\n")
        self.ser.close()
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
def read_conf(filename):
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
#------------------------------------------------------------------------------
class db_client :
	def __init__(self,nomeid,user,id,pwd,dbname):
		self.user=user
		self.id=id
		self.pwd=pwd
		self.dbname=dbname
		self.IDnome=nomeid
		self.queries=[]
		self.backup_flag=[]
		signal.signal(signal.SIGALRM,self.handler)

	def dbserver_add(self,host,dbserver):
		if dbserver == "InfluxDB":
			self.meas="aria"
			query=("curl -H -XPOST 'http://%s/db/write?db=%s&precision=ms' --data-binary '%s,node=%s pm10=%%4.2f,pm25=%%4.2f %%16.0f'" % (host,self.dbname,self.meas,self.IDnome),host+"/aria")
		if dbserver == "CrateDB" :
			query=("curl -H 'Content-Type: application/json' -X POST -d '{\"id_sensor\":%s,\"pm10\":%%4.2f,\"pm25\":%%4.2f,\"user\":\"%s\",\"pwd\":\"%s\",\"created\":%%16.0f}' http://%s/sensor"%(self.id,self.user,self.pwd,host),host)
		self.queries.append(query)
#		print(query)
#		print ("Aggiunto Server",dbserver,"@",host)
		
	def to_db (self,pm10,pm25,logevent):
		ret=""
		for q,h in self.queries:
#			print (h)
			backfile="/home/pi/alfetta/backup_"+h.replace("/","_")
			if self.db_ready(h):
				ret=ret+"I "
				os.system(q%(pm10,pm25,time.time()*1000))
				print (q%(pm10,pm25,time.time()*1000))
				if os.path.exists(backfile):
					logevent.event_log(time.strftime("%H:%M-%a-%b-%d-%Y")+"recover dati per host :"+h+"\n")
					f=open(backfile,"r")
					for l in f :
						print (l)
						os.system(l)
					f.close()
					os.system("cat "+backfile+" >> /home/pi/alfetta/var/log/databuffer.doc")
					os.remove(backfile)
			else:
#				logevent.event_log(time.strftime("%H:%M-%a-%b-%d-%Y")+"backup dati per host :"+h+"\n")
				ret=ret+"B " 
				os.system('echo "'+q%(pm10,pm25,time.time()*1000)+'"'+" >>"+backfile)
#			print(q%(pm10,pm25,time.time()*1000))
#		os.system("curl -H 'Content-Type: application/json' -X POST -d '{\"id_sensor\":1,\"pm25\":%4.2f,\"pm10\":%4.2f,\"user\":\"salvatore\",\"pwd\":\"lippi\"}' 92.223.147.77/nodered/sensor"%(pm25,pm10))
#		c=("curl -i -XPOST 'http://salvatorehost.no-ip.org/db/write?db=ninuxaria&precision=ms' --data-binary 'aria,node=Firenze::Lippi2 pm10=%4.2f,pm25=%4.2f %19.0f'" % (pm10,pm25,time.time()*1000000))
		return(ret)
#
	def handler(self,signum,frame):
		log.event_log(time.strftime("%H:%M-%a-%b-%d-%Y")+"Timeout Event handler"+"\n")
		raise Exception ()

	def db_ready(self,host):
		signal.alarm(5) 
   		try:
        		urllib2.urlopen('http://'+host, timeout=1)
			signal.alarm(0)
        		return True
    		except urllib2.URLError as err:
			signal.alarm(0)
        		return False
		except Exception , exc:
			signal.alarm(0)
			return False

#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
if __name__ == "__main__": 
    basepath="/home/pi/alfetta/"
    configurazione=read_conf(basepath+"etc/alfetta.conf") 
    log = logger(basepath+"var/log/datalog.log",configurazione["nome"])
    log.reset_report()  						#inizializza i valori di report
    log.recover_report()
#    log.send_report()
#    exit(0)
#    for x in configurazione.keys():
#        if (x=="host"):
#            for h in configurazione[x]:
#                print (x+"="+h[0]+","+h[1])
#        else:
#            print (x+"="+configurazione[x])
#    print("\n")
#    time.sleep(3)
    database=db_client(configurazione["nome"],configurazione["user"],configurazione["id"],"lippi","ninuxaria")
    for h in configurazione["host"]:
    	database.dbserver_add(h[0],h[1])

    try:
#--------------------------- SELEZIONE DEL DRIVER DEL SENSORE APPLICATO --------
	if (configurazione["sensore"] == "SDS011") :
        	sensor=sds011_sensor("/dev/ttyUSB0")
	else :
		log.event_log (time.strftime("%H:%M-%a-%b-%d-%Y")+"Nessun sensore conosciuto configurato :",configurazione["sensore"])
		exit(0)
#----------------------------PARTE COMUNE A TUTTI I SENSORI---------------------
	sensor.set_cicletime(2)    # 2 minuti run 3 minuti pausa
	log.event_log (time.strftime("%H:%M-%a-%b-%d-%Y")+"Start\n")
   	while True:
		time.sleep(60) 						# esegue ogni minuto
            	if (sensor.get_status() == "RUNNING") :
			m=sensor.measure("get") 
			if m[2] :
				rr=database.to_db(m[0],m[1],log)
				for r in log.eval_report(m[0],m[1]):
#					print (time.strftime("%H:%M-%a-%b-%d-%Y")+ r)
					log.event_log(time.strftime("%H:%M-%a-%b-%d-%Y")+r+rr+"\n")
#			else :
#				print ("Misure Non Valide")
    except Exception, e:
	sensor.stop_ciclo()
	print (sys.exc_info()[0])
	log.event_log(time.strftime("%H:%M-%a-%b-%d-%Y")+str(e)+"\n")
    	print ("BREAK\n")

