#Coded by PRATIK ANAND pratik@pratikanand.com
import android
import time
import os
from sqlite3 import dbapi2 as sqlite
droid=android.Android()

la={}

def dbreset(passwd):
	print "reset is working"
	con=sqlite.connect('/sdcard/smspass.db')
	cur=con.cursor()
	cur.execute('create table passwd(pass TEXT)')
	cur.execute('insert into passwd values("1234")')
	con.commit()
	
	passwd="1234"
	return passwd


def dbconnection(passwd):
	print "connection is ON"
	con=sqlite.connect('/sdcard/smspass.db')
	cur=con.cursor()
	cur.execute('select * from passwd')
	label=cur.fetchall()
	print label[0][0]
	passwd=label[0][0]
	return passwd





def unread(sender):   #fetch unread messages and send
  #la=droid.smsGetMessageIds(1)
  global la
  print la
  lc=la[1]

  print lc
  print "========" 
  lb={}
  k=0
  for i in lc:
   lb[k]=droid.smsGetMessageById(i)
   k=k+1
   print "***********"
  print "this is lb"
  print lb
  print "this is lb[0]"
  print lb[0]
  print "&&&&&&&&&&"
  print len(lb)
  print "*&*&*&*&"
  print "this is lb[1]"
  print lb[1]
  str=""
  i=0
  #time.sleep(600)
  droid.smsMarkMessageRead(lc,1)
  for i in range(0,len(lb)): 
   str=str+"Sender:"+lb[i][1]['address']+" : "+lb[i][1]['body']+"\n"
  print str
  droid.smsSend(sender,str)
  return



def send(msg,no):    #sending message to a number
    droid.smsSend(no,msg)
    global la
    lc=la[1]
    droid.smsMarkMessageRead(lc,1)
    return


def tts(i):    #reads out a given message
      lb=droid.smsGetMessageById(i)
      global la
      b=lb[1]['body']
      print b
      droid.ttsSpeak(b)
      if(droid.ttsIsSpeaking()):
        droid.makeToast("Text-to-Speech in action")
      
      lm=la[1]
      droid.smsMarkMessageRead(lm,1)
      return

def imei(no):   #sends imei number of the phone(theft control)
  im=droid.getDeviceId()
  str=im[1]
  str="IMEI:"+str
  droid.smsSend(no,str)
  global la
  lc=la[1]
  droid.smsMarkMessageRead(lc,1)

def website(i):  #opens up a website in the phone
  droid.view("http://"+i)
  global la
  lc=la[1]
  droid.smsMarkMessageRead(lc,1)

#def location():   #gives location
#  print droid.readLocation()

def ringer(i):  #set ringer volume
  droid.setRingerVolume(i)
  global la
  lc=la[1]
  droid.smsMarkMessageRead(lc,1)

def toggle_ringer():  #toggle b/w silent and ringer
  droid.toggleRingerSilentMode()
  global la
  lc=la[1]
  droid.smsMarkMessageRead(lc,1)




def check(lc,passwd):   #checking for keyword
  global la 
  la=droid.smsGetMessageIds(1) #id unread msg
  lb=la[1]
  print la
  #print lb
  for i in lb:
    lc=droid.smsGetMessageById(i) #msg by id
    #print lc
    
    if lc:
      #print lc
      str=lc[1]['body'].split()
      
      if "doc" in str and passwd in str:     #key search doc
		 ld=str
		 le=lc[1]
        #print le
		 ld=la[1]
		 ld[0]=i
        #droid.smsMarkMessageRead(lb,1)
		 return lc[1]
    if not lc:
        print "no unread messages"
  return

lc=['ac']
str2="dsadas"
passwd="1234"
droid.dialogCreateSpinnerProgress("Simple Mobile Slave","Joining connections, starting services")
droid.dialogShow()
time.sleep(3)
droid.dialogDismiss()
droid.dialogCreateSpinnerProgress("Simple Mobile Slave","by Pratik Anand")
droid.dialogShow()
time.sleep(3)
droid.dialogDismiss()

#check for db

bool=os.path.exists('/sdcard/smspass.db')
print bool
if(bool==False):
	passwd=dbreset(passwd)
else:
	passwd=dbconnection(passwd)
print passwd
while(1):
 time.sleep(2)
 
 ld=check(lc,passwd)
 if ld:
  str=ld['body'].split()
  print str[2]
  droid.makeToast("Working!!!")
  str2=ld['address']
  print str2
  if str[2]=="unreadmsg":
          unread(str2)
  elif str[2]=="sendmsg":
          uno=str[3]
          i=4
          umsg=""
          while str[i]!="*":
             umsg=umsg+" "+str[i]
             i+=1
          send(umsg,uno)
  elif str[2]=="tts":
          i=str[3]
          tts(int(i))
  elif str[2]=="ringervol":
          i=str[3]
          ringer(int(i))
  elif str[2]=="silent":
          toggle_ringer()
  elif str[2]=="imei":
          str2=str[3]
          imei(str2)
  elif str[2]=="website":
          str2=str[3]
          website(str2)    
 if not ld:
   print "Nothing returned"
   #droid.makeToast("Waiting...")
   