#Created by PRATIK ANAND pratik@pratikanand.com
import android
from sqlite3 import dbapi2 as sqlite
import os
import time

droid = android.Android()
#idea is to test storing of input given to 
#textbox
droid.dialogGetInput("Pincode","Please enter the 4-digt pin")
str=droid.dialogGetResponse()
pin=str[1]['value']
print pin

#insert into db
con=sqlite.connect('/sdcard/smspass.db')
cur=con.cursor()
cur.execute('select * from passwd')
print cur.fetchall()
cur.execute('update passwd set pass='+pin)
cur.execute('select * from passwd')
print cur.fetchall()
con.commit()
droid.makeToast("Pin is [ "+ pin+" ]")
if pin=="1729":
	droid.makeToast("Ramanujan")
droid.dialogCreateSpinnerProgress("Simple Mobile Slave","Password :"+pin)
droid.dialogShow()
time.sleep(1)
droid.dialogDismiss()
#print os.path.exists('/sdcard/test.db')
#print os.path.exists('/sdcard/ninja.db')