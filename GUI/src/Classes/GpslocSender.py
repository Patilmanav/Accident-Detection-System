from jnius import autoclass
from plyer import uniqueid
from plyer import gps
import sqlite3 as sql

from os import environ
from jnius import autoclass

ANDROID_VERSION = autoclass('android.os.Build$VERSION')
SDK_INT = ANDROID_VERSION.SDK_INT

try:
    from android import config
    ns = config.JAVA_NAMESPACE
except (ImportError, AttributeError):
    ns = 'org.renpy.android'

if 'PYTHON_SERVICE_ARGUMENT' in environ:
    PythonService = autoclass(ns + '.PythonService')
    activity = PythonService.mService
else:
    PythonActivity = autoclass(ns + '.PythonActivity')
    activity = PythonActivity.mActivity
  
# Define Java classes
# PythonActivity = autoclass('org.kivy.android.PythonActivity')
SmsManager = autoclass('android.telephony.SmsManager')

# Get the Android context
context = activity



class Send_SMS():
        
    def Start(self):
        
        try:
            def startGPS():
                print("GPS Started")
                try:
                    gps.configure(on_location=onLocation)
                    gps.start()
                except Exception as ex:
                    print("error occured!! ",ex)

            
            def onLocation(**kwargs):
                con = sql.connect('Emergency_contacts.db')
                cur = con.cursor()
                cur.execute("select phone from contact")
                phone = cur.fetchall()
                print("GPS is Accessable....")
                print(kwargs)
                print(f"{kwargs['lat']}\n{kwargs['lon']}")
                varlocation = f"https://maps.google.com/?q={kwargs['lat']},{kwargs['lon']}"
                
                for i in phone:
                    for ph in i:
                        p = ph.split(',')
                        number = p[0]
                        if(p[0].find("+91")!= -1):
                            number = p[0].replace("+91","")
                            
                        phone_number = f'+91{str(number)}'  # Replace with the recipient's phone number
                        print(number)
                        message = f'''I Need Your Help ! \nI have had an accident \nPlease take me from :{varlocation}'''  # Replace with your message
                    
                        sms_manager = SmsManager.getDefault()
                        sms_manager.sendTextMessage(phone_number, None, message, None, None)
                        print("Message Sended to ",phone_number)
                        break
                    
                gps.stop()
            startGPS()
     
        except Exception as ex:
            print("no",ex)
                 
        else:

            print("GPS Project Accomplished!!")
            
            
   