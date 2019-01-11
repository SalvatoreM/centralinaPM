#!/usr/bin/python
import serial, struct, sys, time
import os
import threading

#============================================================================
#---------------------------------------------------------------------------------
class qbit_sensor():
    
    def __init__ (self,dev,log,pm=25):
        print ("sensor QBit init",pm)
        self.ser = serial.Serial()
        self.ser.port = dev
        self.ser.baudrate = 9600
        self.ser.open()
        self.ser.flushInput()
        self.pm=pm
        self.byte, data = 0, ""
        self.pm10k=1
        self.pm10q=0
        self.pm25k=1
        self.pm25q=0
        self.pm10_acc=0
        self.pm25_acc=0
        self.pm10_act=0
        self.pm25_act=0
#-----------------------------------------------------------
#la somma dei due paratri seguenti deve essere sempre = 6
        self.runtime=5    # 1-6 minuti   (1 2 3 4 5 6)
        self.sleeptime=1    # 0-5 minuti   (4 3 2 1 0)
        self.Ton=self.runtime
#-----------------------------------------------------------
#        self.samples=60              # Numero di campioni per media default
        self.Toff=self.sleeptime * 60                 # tempo di pausa Laser OFF Ventola OFF default
        self.samples=12                 # Numero di campioni per media default
        self.sync=0
        self._pm10_acc=0
        self.pm25_acc=0
        self.sample_number=0
#   print ("Cilco abilitato")
        self.sensor_on=threading.Thread(target=self.__ciclo)
        self.lock=threading.Lock()
        self.sensor_on.start()
        self.status="PAUSE"
	self.log=log
	self.run=True
	self.pm10=0
	self.pm25=0
        self.estop=threading.Event()
        self.sensor_on=threading.Thread(target=self.__ciclo)
        self.lock=threading.Lock()
#   print ("Init End")

    def get_status(self):
        return(self.status)


    def set_pm10_calibration (self,kk,k,q):
        self.pm10kk=float(kk)
        self.pm10k=float(k)
        self.pm10q=float(q)

    def set_pm25_calibration (self,kk,k,q):
        self.pm25kk=float(kk)
        self.pm25k=float(k)
        self.pm25q=float(q)

    def autocalibration(self,isgnum,frame):
        self.log.event (time.strftime("%H:%M-%a-%b-%d-%Y")+"Aggiornamento Parametri di Calibrazione\n")
        basepath="/home/pi/alfetta/"
        configurazione=read_conf(basepath+"etc/alfetta.conf")
        self.log.event(time.strftime("%H:%M-%a-%b-%d-%Y")+"PM2.5 ",configurazione["kk2"],configurazione["k2"],configurazione["q2"])
        self.log.event(time.strftime("%H:%M-%a-%b-%d-%Y")+"PM10 ",configurazione["kk1"],configurazione["k1"],configurazione["q1"])
        self.set_pm10_calibration(configurazione["kk1"],configurazione["k1"],configurazione["q1"])
        self.set_pm25_calibration(configurazione["kk2"],configurazione["k2"],configurazione["q2"])
        b='echo "nome=%s\nkk1=%s\nk1=%s\nq1=%s" > /var/www/html/alfetta/correction.conf' %(configurazione["nome"],configurazione["kk1"],configurazione["k1"],configurazione["q1"])
        os.system(b)
        b='echo "kk2=%s\nk2=%s\nq2=%s" >> /var/www/html/alfetta/correction.conf' %(configurazione["kk2"],configurazione["k2"],configurazione["q2"])
        os.system(b)

    def cmd_query_data(self):
        l={}
        rcv = self.read_response()  #Sospensiva ?
        rcv=rcv.replace("\r","")
        if "PM:" in rcv:
#            rcv=rcv.replace("\r","")
#            print ("Primo split:",rcv.split('|'))
            print (time.strftime("%H:%M:%S"),"-----------------------------")
            lrcv=rcv.split("|")
            for e in lrcv:
#                e.replace("\r","")
                val=e.split(":")
                if len(val)==2 :
                    print (val[0],val[1])
                if val[0].replace(" ","") == "PM" :
                    l["pm10"]=val[1]
                    l["pm25"]=val[1]
                    if self.pm==10 :
                        self.pm10=int(val[1])
                    if self.pm==25 :
                        self.pm25=int(val[1])
                if val[0].replace(" ","") =="T" :
                    self.t=float(val[1])
                if val[0].replace(" ","") =="P" :
                    self.p=float(val[1])
                if val[0].replace(" ","") =="rH" :                  
                    self.rh=float(val[1])
        else:
            self.pm25=0
            self.pm10=0

    def read_response(self):
        byte = ""
        r=""
        while byte != "\n":
            byte=self.ser.read(1)
            if (byte != "\n" ):
                r=r+byte
#        print "Risposta =",r
        return r

    def cmd_set_sleep(self,sleep=1):
        if sleep == 0 : 
            self.ser.write("stop\n\r")
            self.status="PAUSE"
        else :
            self.ser.write("start\n\r")
            self.status="RUNNING"
        self.read_response()
 
#    def set_cicletime(self,runtime):
#            runtime=1

    def set_cicletime(self,runtime):
        if runtime > 5 :
            self.runtime=5
        elif runtime < 1 :
            self.runtime=1
#-----------------------------------------------------------
#la somma dei due parametri seguenti deve essere sempre = 6
#-----------------------------------------------------------
        else :
            self.runtime=runtime             # 1-6 minuti   (1 2 3 4 5) tempo di acquisione misure
        self.sleeptime=(5 - self.runtime)    # 0-5 minuti   (4 3 2 1 0) tempo di pausa (Laser OFF Fan OFF)
#-----------------------------------------------------------
        self.samples=12                      # Numero di campioni per media default
        self.Toff=self.sleeptime * 60        # tempo di pausa Laser OFF Ventola OFF default
        self.Ton=self.runtime

    def get_runtime(self):
        return(self.runtime)

    def get_sleeptime(self):
        return(5-self.runtime)

    def set_pm10_calib(self,k,q):
        self.pm10k=k
        self.pm10q=q
            
    def set_pm25_calib(self,k,q):
        self.pm25k=k
        self.pm25q=q

    def elaborate (self):
        if self.pm==10 :
            self.pm10_acc=self.pm10_acc+((self.pm10kk*self.pm10*self.pm10)+self.pm10k*self.pm10+self.pm10q)/self.samples
        if self.pm==25 :
            self.pm25_acc=self.pm25_acc+((self.pm25kk*self.pm25*self.pm25)+self.pm25k*self.pm25+self.pm25q)/self.samples

    def measure(self,op):
        try:
            self.lock.acquire()
            if op=="update" :
                print ("Update\n")
                self.update_measure()
            if  op =="get":
                print ("Get\n")
                return(self.get_measure())
        finally:
            self.lock.release()
 
    def update_measure(self):
        self.pm10_act = self.pm10_acc
        self.pm25_act = self.pm25_acc
        self.t_act=self.t
        self.p_act=self.p
        self.rh_act=self.rh 
        self.validate=True
        print (self.pm10_act,self.pm25_act)
        self.pm10_acc=0
        self.pm25_acc=0  
        
    def get_measure(self):
        pm10_tmp=self.pm10_act
        pm25_tmp=self.pm25_act
        return (pm10_tmp,pm25_tmp,self.validate)

    def stop_ciclo(self):
        print ("Stop ciclo Comandato")
        self.estop.set()
        self.run= False
        self.sensor_on.join()
        return(True)

#   def stop_ciclo(self):
#        self.sensor_on.do_run=False
#        self.sensor_on.join()
#        return(True)

    def __ciclo(self):
        time.sleep(5)
        print ("partito")
        self.validate = False
        self.cmd_set_sleep(0)
        time.sleep(3)
        Ton=self.runtime
        self.Toff=self.sleeptime*60
        print ("Toff=",self.Toff,"Ton=",self.Ton)
        Tmedia=self.samples   #12 campioni uno ogni 5 secondi
#        self.cmd_set_mode(1);
#        time.sleep(2)
#        self.log.event_log(time.strftime("%H:%M-%a-%b-%d-%Y")+" Test Sensor Mode\n")
#        while not (self.test_query_mode()):
#            self.cmd_set_mode(1)
#            time.sleep(2)
#        time.sleep(3)
#        self.log.event_log(time.strftime("%H:%M-%a-%b-%d-%Y")+" Test Superato \n")
        try :
            print ("In Ciclo Ton= %d Toff=%d \n" %(self.Ton,self.Toff))
            self.log.event_log(time.strftime("%H:%M-%a-%b-%d-%Y")+" In Ciclo Ton= %d minuti Toff=%d secondi \n" %(self.Ton,self.Toff))
            while self.run:
                if (self.Toff > 30 ):
                    print (time.strftime("%H:%M:%S"),"PAUSE",self.get_sleeptime())
                    b='echo "'+time.strftime("%H:%M:%S")+' PAUSE %d %4.2f %4.2f" > /var/www/html/alfetta/sensor.log' %((self.get_sleeptime()*60)-30,self.pm10,self.pm25)
                    os.system(b) 
                    self.status="PAUSE"
                    self.cmd_set_sleep(0)
                    if self.estop.wait(self.Toff) :
                        print ("STOP 1")
                        raise ValueError('Recevived Stop')
                    self.cmd_set_sleep(1)
                    print (time.strftime("%H:%M:%S"),"RUNNING", self.get_runtime())
                    self.status="RUNNING"
		    self.running_start=time.time()
		    while ((time.time()-self.running_start) < (self.Ton*60)):
                        print ("Tempo= ",(time.time()-self.running_start))
                        for i in range (1,Tmedia+1):
                            inizio=time.time()
			    print ("----",i,"-----\n")
                            self.cmd_query_data();
                            self.elaborate()             # esegue per ora solo la media 
                            b='echo "'+time.strftime("%H:%M:%S")+' RUNNING %d %4.2f %4.2f" > /var/www/html/alfetta/sensor.log' %(self.get_runtime()*60,self.pm10,self.pm25)
                            os.system(b) 
                            self.sample_number=i
                            if self.estop.wait(1):
                                print ("STOP 3")
                                raise ValueError('Recevived Stop')
                        self.measure("update")
                    print ("Tempo Totale= ",(time.time()-self.running_start))
            self.cmd_set_sleep(0)
        except Exception as  e:
            self.log.event_log(time.strftime("%H:%M-%a-%b-%d-%Y")+str(e)+"\n")
            pass
        print ("Qbit\n")
        self.ser.close()
#------------------------------------------------------------------------------


