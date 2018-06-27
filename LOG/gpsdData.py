import sys
import os
from gps import *
import time
import threading
import IMU
import zlib, base64
from firebase import firebase
from picamera import PiCamera
import urllib2, urllib, httplib
from threading import Thread, Event
import requests
import errno
from socket import error as SocketError
 
stop_event = Event()
 
 
#when internet is not connected it will retry sending data
def do_actions(dic,dt):
        retry_on = (requests.exceptions.Timeout,requests.exceptions.ConnectionError,requests.exceptions.HTTPError)
        time_out=3
        while True:
                try:
                        firebase.post(dic,dt)
                except retry_on:
                        time.sleep(time_out)
                        continue
                else:
                        break

#checks it internet connection is available
def internet_on():
	exc = (urllib2.URLError, urllib2.HTTPError)
	try:
		urllib2.urlopen('http://216.58.192.142',timeout=3)
		return True
	except exc:			
                return False
	except socket.timeout:
		return False
	except SocketError as e:
		if e.errno !=errno.ECONNRESET:
			raise
		pass
 
#Sampling rate is 30 sec...Writing the recorded data to the firebase 
def writeLog(string,f):
      
      flag = 0  
      localtime = time.asctime(time.localtime(time.time()))
      print('latitude    ' , gpsd.fix.latitude)
      print('longitude   ' , gpsd.fix.longitude)
      print('Time        ' , localtime)
      string1 = '/home/pi/Documents/LOG/images/img%s.jpg'%(localtime)
      camera=PiCamera()
      camera.capture(string1)
      camera.close()
      print(string1)
      imag=string1
	  #encoding jpeg to text and compressing the text
      with open(imag,"rb") as imageFile:
       image_64= base64.b64encode(zlib.compress(imag,9))
      data="Time:%s\tLat:%f\tLong:%f\tImage:%s\tImgAsTxt:%s\tAccFile:%s" %(localtime,gpsd.fix.latitude,gpsd.fix.longitude,string1,image_64,string)  
      f.write("\n%s\n" %data)     
      result=internet_on()
      if result:
           if os.path.exists("/home/pi/Documents/LOG/data.txt"):
                   f_noc=open("/home/pi/Documents/LOG/data.txt","a+")
                   f_noc.seek(0,0)
                   lines=f_noc.readlines()
                   if lines!='':
                           for x in lines:
                                   if flag==0:
                                       action_thread = Thread(target=do_actions,args=('\LOG',x,))
                                       action_thread.start()
                                       flag=1
                                   else:
                                       a=x.splitlines()
                                       z=a[0]
                                       u=open(z,"r+")
                                       v=u.readlines()
                                       action_thread = Thread(target=do_actions,args=('\AccFile',v,))
                                       action_thread.start()
                                       flag=0
                                       u.close()        
                           os.remove("/home/pi/Documents/LOG/data.txt")
           
           t=open(string,"r+")
           s=t.readlines() 
           action_thread = Thread(target=do_actions,args=('\AccFile',s,))
           action_thread.start()
           t.close()
           action_thread = Thread(target=do_actions,args=('\LOG',data,))
           action_thread.start()
          
      else:
           f_noc=open("/home/pi/Documents/LOG/data.txt","a+")   
           datafile='%s\n%s\n'%(data,string)
           f_noc.write("%s"%datafile)    
      return     


	  
#Beginning of the program
IMU.detectIMU()
IMU.initIMU()
gpsd = None

f=open("/home/pi/Documents/LOG/LOG.txt","a+")
#Your database name in firebase
firebase=firebase.FirebaseApplication('https://<YOUR_DATABASE_NAME>.firebaseio.com/', None)

os.system('clear')
 
class GpsPoller(threading.Thread):
  def __init__(self):
    threading.Thread.__init__(self)
    global gpsd
    gpsd = gps(mode=WATCH_ENABLE) 
    self.current_value = None
    self.running = True
 
  def run(self):
    global gpsd
    while gpsp.running:
      gpsd.next() 
if __name__ == '__main__':
  gpsp = GpsPoller() 
  gpsp.start()
count=0
while True:
    count=count+1
    print(count)
    local = time.asctime(time.localtime(time.time()))
    string = '/home/pi/Documents/LOG/accel/acc%s.txt'%local
    acc='/accel/acc%s'%local
    fa=open(string,"a+")
	#collecting the value of accelerometer every .5 sec So 60 values in 30sec
    for x in range(60):
      ACCx=IMU.readACCx()
      ACCy=IMU.readACCy()
      ACCz=IMU.readACCz()
      x=((ACCx*0.244)/100)
      y=((ACCy*0.244)/100)
      z=((ACCz*0.244)/100)
      print("X = %f\t"%x),
      print("Y = %f\t"%y),
      print("Z = %f\t"%z)    
      ts=time.gmtime()
      str2 = "X = %f\tY = %f\tZ=%f"%(x,y,z)
      str1 = (time.strftime("%x %X",ts))
      fa.write("%s\t\t%s\n"%(str2,str1))
      time.sleep(0.5)
    fa.close()
    writeLog(string,f)
    
    
f.close()
