#!/usr/bin/python
#coding=utf-8
import serial, struct, sys, time, os
import threading
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
    
    def __init__ (self,dev,log):
        self.ser = serial.Serial()
        self.ser.port = dev
        self.ser.baudrate = 9600
        self.ser.open()
        self.ser.flushInput()
        self.byte, data = 0, ""
        self.pm10=0
        self.pm25=0
        self.pm10kk=0
        self.pm10k=1
        self.pm10q=0
        self.pm25kk=0
        self.pm25k=1
        self.pm25q=0
        self.pm10_acc=0
        self.pm25_acc=0
        self.pm10_act=0
        self.pm25_act=0
#-----------------------------------------------------------
#la somma dei due paratri seguenti deve essere sempre = 6
        self.runtime=5      # 1-5 minuti   (1 2 3 4 5)
        self.sleeptime=1    # 0-5 minuti   (4 3 2 1 0)
        self.Ton=self.runtime
        self.samples=60              		      # Numero di campioni per media default
        self.Toff=self.sleeptime * 60                 # tempo di pausa Laser OFF Ventola OFF default
#-----------------------------------------------------------
        self.sync=0
        self.pm10_acc=0
        self.pm25_acc=0
#        self.sample_number=0
        self.estop=threading.Event()
        self.sensor_on=threading.Thread(target=self.__ciclo)
        self.lock=threading.Lock()
        time.sleep(1)
        self.sensor_on.start()
        self.status="PAUSE"
        self.run=True
	self.log=log

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
        self.samples=60                      # Numero di campioni per media default
        self.Toff=self.sleeptime * 60        # tempo di pausa Laser OFF Ventola OFF default
	self.Ton=self.runtime

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
        checksum = sum(ord(v) for v in d[2:8])%256
        if (checksum==r[2] and r[3]==0xab):
            self.pm25 = r[0]/10.0
            self.pm10 = r[1]/10.0
        else:
            self.pm10=0
            self.pm25=0
        
    def process_version(self,d):
        r = struct.unpack('<BBBHBB', d[3:])
        checksum = sum(ord(v) for v in d[2:8])%256
 
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


    def test_query_mode(self):
        self.ser.write(self.construct_command(self.CMD_MODE, [0x0, 0x0]))
        d=self.read_response()
        if d[2].encode("hex") == "\x02".encode("hex") :
                if d[4].encode("hex") == "\x01".encode("hex") :
                  return(1) # query mode : Sensor received query data command to report a measurement data.
        else:
                return (0) #active mode ：Sensor automatically reports a measurement data in a work period.
 
    def cmd_query_data(self):
        self.ser.write(self.construct_command(self.CMD_QUERY_DATA))
        d = self.read_response()
        if d[1].encode("hex") == "\xc0".encode("hex"):
            self.process_data(d)
        else:
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
        self.pm10_acc=self.pm10_acc+((self.pm10kk*self.pm10*self.pm10)+self.pm10k*self.pm10+self.pm10q)/self.samples
        self.pm25_acc=self.pm25_acc+((self.pm25kk*self.pm25*self.pm25)+self.pm25k*self.pm25+self.pm25q)/self.samples

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
        pm10_tmp=self.pm10_act
        pm25_tmp=self.pm25_act
        return (pm10_tmp,pm25_tmp,self.validate)

    def stop_ciclo(self):
    	print ("Stop ciclo Comandato")
        self.estop.set()
    	self.run= False
    	self.sensor_on.join()
    	return(True)
            
    def __ciclo(self):
        time.sleep(5)
        print ("partito")
        self.validate = False
#        self.cmd_set_sleep(1)
        Ton=self.runtime
        self.Toff=self.sleeptime*60
        print ("Toff=",self.Toff,"Ton=",self.Ton)
        Tmedia=self.samples
        self.cmd_set_mode(1);
        time.sleep(2)
        self.log.event_log(time.strftime("%H:%M-%a-%b-%d-%Y")+" Test Sensor Mode\n")
        while not (self.test_query_mode()):
            self.cmd_set_mode(1)
            time.sleep(2)
        time.sleep(3)
        self.log.event_log(time.strftime("%H:%M-%a-%b-%d-%Y")+" Test Superato \n")
        try :
            print ("In Ciclo Ton= %d Toff=%d \n" %(self.Ton,self.Toff))
            self.log.event_log(time.strftime("%H:%M-%a-%b-%d-%Y")+" In Ciclo Ton= %d minuti Toff=%d secondi \n" %(self.Ton,self.Toff))
            while self.run:
                if (self.Toff > 30 ):
                    print (time.strftime("%H:%M:%S"),"PAUSE",self.get_sleeptime())
                    b='echo "'+time.strftime("%H:%M:%S")+' PAUSE %d %4.2f %4.2f" > /var/www/html/alfetta/sensor.log' %((self.get_sleeptime()*60)-30,self.pm10,self.pm25)
                    os.system(b) 
                    self.status="PAUSE"
                    self.cmd_set_sleep(1)
#                    time.sleep(Toff-30)
                    if self.estop.wait(self.Toff-30) :
                        print ("STOP 1")
                        raise ValueError('Recevived Stop')
#                    time.sleep(Toff-30)
                    self.status="PRE RUNNING"
                    print(time.strftime("%H:%M:%S"),"PRE RUNNING")
                    b='echo "'+time.strftime("%H:%M:%S")+' PRE_RUNNING %d %4.2f %4.2f" > /var/www/html/alfetta/sensor.log' %(30,self.pm10,self.pm25)
                    os.system(b) 
                    self.cmd_set_sleep(0)
                    if self.estop.wait(30):
                        print ("STOP 2")
                        raise ValueError('Recevived Stop')
#                    time.sleep(30)         # accensione 
                    print (time.strftime("%H:%M:%S"),"RUNNING", self.get_runtime())
                    self.status="RUNNING"
                    for j in range(1,self.Ton+1):
                        for i in range (1,Tmedia+1):
                            inizio=time.time()
                            self.cmd_query_data();
                            self.elaborate()             # esegue per ora solo la media 
                            b='echo "'+time.strftime("%H:%M:%S")+' RUNNING %d %4.2f %4.2f" > /var/www/html/alfetta/sensor.log' %(self.get_runtime()*60,self.pm10,self.pm25)
                            os.system(b) 
#                            self.sample_number=i
                            if self.estop.wait(1):
                                print ("STOP 3")
                                raise ValueError('Recevived Stop')
#                           time.sleep(1)
                        self.measure("update")
            self.cmd_set_sleep(1)
        except Exception as  e:
            self.log.event_log(time.strftime("%H:%M-%a-%b-%d-%Y")+str(e)+"\n")
            pass
        print ("SDS011STOP\n")
        self.ser.close()
#------------------------------------------------------------------------------

