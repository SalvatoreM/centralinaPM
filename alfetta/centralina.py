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
import glob
import re
#============================================================================
#============================================================================
class logger():
    def __init__(self,logfile,name):
#       print ("init Logger")
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
        self.year=time.strftime("%y")
        filename=string.split(logfile,"/")
        for f in filename[:-1]:
            self.path=self.path+f+"/"
        for f in filename[-1:]:
            self.name=self.name+f
#        print self.path+self.name
        if (not os.path.isfile(self.path+self.name)):
            dfile = open (self.path+self.name,"w")
            dfile.write ("Nuovo File del "+time.strftime("%c")+"\n")
            dfile.close
#        print ("logger installed")
#============================================================================
#============================================================================
    def event_log(self,message):
        dfile = open (self.path+self.name,"a")
        dfile.write (message)
        dfile.close()
        self.archive()
#============================================================================
#============================================================================
    def archive(self):
        if (time.strftime("%H:%M") >= "00:00" and time.strftime("%H:%M") <"00:30"):
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
            if (not self.report):
                f=open("/home/pi/alfetta/etc/mail_account","r")
                self.account=string.split(f.read(),"\n")
                f.close()
                if (string.split(self.account[0],"#")[1]  == "yes"):
                    print (self.account)
                    self.user=string.split(self.account[2],"#")[1]
                    self.passw=string.split(self.account[3],"#")[1]
                    self.sender=string.split(self.account[5],"#")[1]
                    self.receiver=string.split(self.account[6],"#")[1]
                    self.provider=string.split(self.account[1],"#")[1]
                    self.port=string.split(self.account[4],"#")[1]
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
                    if self.pm10_day > 50 :
                        self.testo=self.testo+"Oggi  il limite di legge (50 ug/m3)  per il PM10 è stato superato"+"\n\n\n"
                    if self.pm25_day > 25 :
                        self.testo=self.testo+"Oggi  il limite di legge (25 ug/m3)  per il PM2.5 è stato superato"+"\n\n\n"
                    if self.pm10_day > 20 :
                        self.testo=self.testo+"Oggi  il limite OMS (20 ug/m3)  per il PM10 è stato superato"+"\n\n\n"
                    if self.pm25_day > 10 :
                        self.testo=self.testo+"Oggi  il limite OMS (10 ug/m3)  per il PM2.5 è stato superato"+"\n\n\n"
                    try:
                        if (self.port != "0" ) :
                            self.server=smtplib.SMTP(self.provider,self.port)
                        else :
                            self.server=smtplib.SMTP(self.provider)
                        self.server.login(self.user,base64.b64decode(self.passw))
                        self.oggetto="Report Centralina Qualità dell'aria"
                        self.messaggio="From:%s\nTo:%s\nSubject:%s\n\n%s" %(self.sender,self.receiver,self.oggetto,self.testo)
                        self.server.sendmail(self.sender,self.receiver,self.messaggio)
                        self.server.quit()
                        self.event_log ("["+time.strftime("%c")+"] "+ "Report del giorno "+time.strftime("%A %B %d %Y")+" --"+ " INVIATO a "+self.receiver+"\n")
                    except:
                        self.event_log ("["+time.strftime("%c")+"] "+ "Report del giorno "+time.strftime("%A %B %d %Y")+" --"+ "  NON INVIATO a "+self.receiver+"\n")
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
                if (time.strftime("%y") != self.year) :
                    self.year=time.strftime("%y")
#                if (time.strftime("%d%m") =="0101") :
                    self_pm10_year=self.pm10_y
                    self.pm25_year=self.pm25_y
                    self.n_day=0
                    self.pm10_over=0
                    self.pm10_over_OMS=0
                    self.pm25_over=0
                    self.pm25_over_OMS=0
            self.save_report()
#-------------------------------------------------------------------------------
        retpm10=" PM10  |"
        retpm10=retpm10+(" % 3.2f"%(pm10)).center(8)
        retpm10=retpm10+"|"+(" % 3.2f"%(self.pm10_medio)).center(8)
        retpm10=retpm10+"|"+(" % 3.2f"%(self.pm10max)).center(8)
        retpm10=retpm10+"|"+(" % 3.2f"%(self.pm10min)).center(8)+"|"
        retpm25=" PM2.5 |"
        retpm25=retpm25+(" % 3.2f"%(pm25)).center(8)
        retpm25=retpm25+"|"+(" % 3.2f"%(self.pm25_medio)).center(8)
        retpm25=retpm25+"|"+(" % 3.2f"%(self.pm25max)).center(8)
        retpm25=retpm25+"|"+(" % 3.2f"%(self.pm25min)).center(8)+"|"
        print ("Anno ",self.year)
        return(retpm10,retpm25)
#============================================================================
#============================================================================
    def reset_report (self):
        self.n=0
        self.n_ore=0
        self.pm10_day=0
        self.pm10_h=0
        self.pm10max=0
        self.pm10min=2000
        if (time.strftime("%y") != self.year):
            self.pm10_over=0
            self.pm10_over_OMS=0
        self.pm25_day=0
        self.pm25_h=0
        self.pm25max=0
        self.pm25min=2000
        if (time.strftime("%y") != self.year):
            self.year=time.strftime("%y")
            self.pm25_over=0
            self.pm25_over_OMS=0
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
        f.write("self.pm25maxt="+"'%s'\n"%(self.pm25maxt))                    
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
            print ("Anno ",self.year)

#============================================================================
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
def autocalibration(isgnum,frame):
   global configurazione
   log.event_log (time.strftime("%H:%M-%a-%b-%d-%Y")+" Aggiornamento Parametri di Calibrazione\n")
   basepath="/home/pi/alfetta/"
   configurazione=read_conf(basepath+"etc/alfetta.conf")
   log.event_log(time.strftime("%H:%M-%a-%b-%d-%Y")+" PM2.5 :"+" kk2="+configurazione["kk2"]+" k2="+configurazione["k2"]+" q2="+configurazione["q2"]+"\n")
   log.event_log(time.strftime("%H:%M-%a-%b-%d-%Y")+" PM10  :"+" kk1="+configurazione["kk1"]+" k1="+configurazione["k1"]+" q1="+configurazione["q1"]+"\n")
   sensor.set_pm10_calibration(configurazione["kk1"],configurazione["k1"],configurazione["q1"])
   sensor.set_pm25_calibration(configurazione["kk2"],configurazione["k2"],configurazione["q2"])
   b='echo "nome=%s\nkk1=%s\nk1=%s\nq1=%s" > /var/www/html/alfetta/correction.conf' %(configurazione["nome"],configurazione["kk1"],configurazione["k1"],configurazione["q1"])
   os.system(b)
   b='echo "kk2=%s\nk2=%s\nq2=%s" >> /var/www/html/alfetta/correction.conf' %(configurazione["kk2"],configurazione["k2"],configurazione["q2"])
   os.system(b)

#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
class db_client :
    def __init__(self,nomeid,user,id,pwd,dbname,mac):
        self.user=user
        self.id=id
        self.pwd=pwd
        self.dbname=dbname
        self.IDnome=nomeid
        self.queries=[]
        self.backup_flag=[]
        self.tobe_remote=1
        self.mac=mac
        signal.signal(signal.SIGALRM,self.handler)

    def dbserver_add(self,host,dbserver):
        if dbserver == "InfluxDB":
            self.meas="aria"
            query=("curl -H -XPOST 'http://%s/db/write?db=%s&precision=ms' --data-binary '%s,node=%s nome=\"%s\",pm10=%%4.2f,pm25=%%4.2f %%16.0f'" % (host,self.dbname,self.meas,self.mac,self.IDnome),host+"/aria")
        if dbserver == "CrateDB" :
            query=("curl -H 'Content-Type: application/json' -X POST -d '{\"id_sensor\":%s,\"pm10\":%%4.2f,\"pm25\":%%4.2f,\"user\":\"%s\",\"pwd\":\"%s\",\"created\":%%16.0f}' http://%s/rest"%(self.id,self.user,self.pwd,host),host)
        self.queries.append(query)
        
    def to_db (self,pm10,pm25,logevent):
        ret=""
        for q,h in self.queries:
            backfile="/home/pi/alfetta/backup_"+h.replace("/","_")
            if self.db_ready(h):
                if (self.tobe_remote):
                    os.system("/home/pi/alfetta/send_remote.sh")
                    self.tobe_remote=0
                ret=ret+"I "
                os.system(q%(pm10,pm25,time.time()*1000))
                print (q%(pm10,pm25,time.time()*1000))
                if os.path.exists(backfile):
                    logevent.event_log(time.strftime("%H:%M-%a-%b-%d-%Y")+"recover dati per host :"+h+"\n")
                    f=open(backfile,"r")
                    for l in f :
                        try :
                            os.system(l)
                        except:
                            pass
                    f.close()
                    os.remove(backfile)
            else:
                ret=ret+"B "
                b=q%(pm10,pm25,time.time()*1000)
                b="echo \""+b.replace("\"","\\\"")+"\" >>"+backfile
                os.system(b) 
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
            log.event_log(time.strftime("%H:%M-%a-%b-%d-%Y ")+err.message+"\n")
            signal.alarm(0)
            return False
        except Exception , exc:
            log.event_log(time.strftime("%H:%M-%a-%b-%d-%Y ")+exc.message+"\n")
            signal.alarm(0)
            return False

#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
if __name__ == "__main__":
    _version = "1.0" 
    exit = threading.Event()
    basepath="/home/pi/alfetta/"
    configurazione=read_conf(basepath+"etc/alfetta.conf") 
    log = logger(basepath+"var/log/datalog.log",configurazione["nome"])
    log.reset_report()                          #inizializza i valori di report
    log.recover_report()
#    b='echo "Centralina.py Ver '+_version+'" > /var/www/html/alfetta/version.log'
    b='cat /home/pi/alfetta/version  > /var/www/html/alfetta/version.log'
    os.system(b) 
    time.sleep(2)
#    mac=os.popen("/sbin/ifconfig wlan0 |grep HWaddr|cut -d' ' -f10").read().replace("\n","")
    mac=""
    if not (re.match("[0-9a-f]{2}([-:]?)[0-9a-f]{2}(\\1[0-9a-f]{2}){4}$", mac.lower())):
        mac=os.popen("/sbin/ifconfig wlan0 |grep -E 'HWaddr|ether'|cut -d' ' -f10").read().replace("\n","")
    mac=mac.replace(":","_")
    database=db_client(configurazione["nome"],configurazione["user"],configurazione["id"],configurazione["pswdb"],"ninuxaria",mac)
    for h in configurazione["host"]:
        database.dbserver_add(h[0],h[1])

#--------------------------- SELEZIONE DEL DRIVER DEL SENSORE APPLICATO --------
    try:
	print (configurazione["sensore"],configurazione["sensore"].split(",")[0])
        if (configurazione["sensore"] == "SDS011") :
            import lsds011
            serfound = False
            for s in glob.glob('/dev/tty[SU]*'):
                print (s)
                if ((s == "/dev/ttyUSB0") or (s == "/dev/ttyUSB1") or (s == "/dev/ttyS0")) :
#                if ((s == "/dev/ttyUSB0") or (s == "/dev/ttyS0")) :
                  sensor=lsds011.sds011_sensor(s,log)
                  if (sensor):
                     serfound = True
                     sensor.set_cicletime(2)    # 2 minuti run 3 minuti pausa
                     break
            if (not serfound) :
                print ("Stop Ciclo!!!! Serial Device Not Found")
                log.event_log(time.strftime("%H:%M-%a-%b-%d-%Y")+"STOP:Serial port device not found\n")
                sys.exit(1)
        elif (configurazione["sensore"].split(",")[0] == "QBIT"):
            print ("Install Qbit drive")
#            print (imported("lqbit"))
#            if not imported("lqbit"):
#                import lqbit
            import lqbit
#            sensor=lqbit.qbit_sensor("/dev/ttyUSB0")
            serfound = False
            for s in glob.glob('/dev/tty[SU]*'):
                print (s)
                if ((s == "/dev/ttyUSB0") or (s == "/dev/ttyUSB1") or (s == "/dev/ttyS0")) :
                  confpm=configurazione["sensore"].split(",")[1]
                  sensor=lqbit.qbit_sensor(s,log,int(confpm))
                  if (sensor):
                     serfound = True
                     sensor.set_cicletime(4)    # 4 minuti run 1 minuti pausa
                     break
            if (not serfound) :
                print ("Stop Ciclo!!!! Serial Device Not Found")
                log.event_log(time.strftime("%H:%M-%a-%b-%d-%Y")+"STOP:Serial port device not found\n")
                sys.exit(1)

        else :
            log.event_log (time.strftime("%H:%M-%a-%b-%d-%Y")+"Nessun sensore conosciuto configurato :",configurazione["sensore"])
            exit(0)
#----------------------------PARTE COMUNE A TUTTI I SENSORI---------------------
#        sensor.set_cicletime(2)    # 2 minuti run 3 minuti pausa
        sensor.set_pm10_calibration(configurazione["kk1"],configurazione["k1"],configurazione["q1"])
        sensor.set_pm25_calibration(configurazione["kk2"],configurazione["k2"],configurazione["q2"])
        b='echo "nome=%s\nkk1=%s\nk1=%s\nq1=%s" > /var/www/html/alfetta/correction.conf' %(configurazione["nome"],configurazione["kk1"],configurazione["k1"],configurazione["q1"])
        os.system(b) 
        b='echo "kk2=%s\nk2=%s\nq2=%s" >> /var/www/html/alfetta/correction.conf' %(configurazione["kk2"],configurazione["k2"],configurazione["q2"])
        os.system(b) 
        time.sleep(5)
        log.event_log (time.strftime("%H:%M-%a-%b-%d-%Y")+"Start SDSO11.py vers "+_version+"\n")
        log.event_log (time.strftime("%H:%M-%a-%b-%d-%Y")+"Sensor is running in Query Mode : Waiting to Start\n")
#       Intercetta trigger USR1 (#pkill --signal SIGUSR1 sds011.py )per modifica parametri di taratura
        signal.signal(signal.SIGUSR1,autocalibration)
        while not exit.is_set() :
            if (sensor.get_status() == "RUNNING") :
               m=sensor.measure("get") 
               print ("Acquisita misura\n")
               if m[2] :
                    rr=database.to_db(m[0],m[1],log)
		    print ("Inviata misura\n",m[0],m[1])
                    for r in log.eval_report(m[0],m[1]):
                        log.event_log(time.strftime("%H:%M-%a-%b-%d-%Y")+r+rr+"\n")
            exit.wait(60)
    except KeyboardInterrupt, e:
        print ("Stop Ciclo!!!!")
        sensor.stop_ciclo()
        log.event_log(time.strftime("%H:%M-%a-%b-%d-%Y")+"Keyboard_STOP:___"+str(e)+"\n")
    	print ("BREAK\n")
    except Exception, e:
        print ("Stop Ciclo!!!!")
        sensor.stop_ciclo()
        log.event_log(time.strftime("%H:%M-%a-%b-%d-%Y")+"Unattended_STOP:...."+str(e)+"\n")
    	print ("BREAK\n")


