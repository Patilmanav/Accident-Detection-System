from kivy.app import App
from kivy.uix.widget import Widget
from jnius import autoclass
from plyer import uniqueid
from plyer import gps

# Define Java classes
PythonActivity = autoclass('org.kivy.android.PythonActivity')
SmsManager = autoclass('android.telephony.SmsManager')

# Get the Android context
context = PythonActivity.mActivity



class MyWidget(Widget):
    
    def on_submit(self):
        try:
            phn = "9619994541"
            print(int(phn))
            self.get_location(phn)
            print("onsubmit...")
        
        except Exception as ex:
            print("Enter Correct Number",ex)
            self.ids.lbl.text = f"Enter Correct Number, {ex}"
            
        
    def get_location(self,ph):
        try:
            def startGPS():
                print("GPS Started")
                try:
                    gps.configure(on_location=onLocation)
                    gps.start()
                except Exception as ex:
                    print("error occured!! ",ex)


            def onLocation(**kwargs):
                print("GPS is Accessable....")
                print(kwargs)
                print(f"{kwargs['lat']}\n{kwargs['lon']}")
                varlocation = f"https://maps.google.com/?q={kwargs['lat']},{kwargs['lon']}"
                
                
                phone_number = f'+91{ph}'  # Replace with the recipient's phone number
                message = varlocation  # Replace with your message
            
                sms_manager = SmsManager.getDefault()
                sms_manager.sendTextMessage(phone_number, None, message, None, None)
                print("Message Sended")
                self.ids.lbl.text = "Send Successfully"
                
            startGPS()
     
        except Exception as ex:
            print("no",ex)
            self.ids.lbl.text = f"Error Found: {ex}"
                 
        else:

            print("GPS Project Accomplished!!")
            
            
   

        
        

class gpsSenderApp(App):

    def build(self):
        
        return MyWidget()
    
if __name__ == '__main__':
    gpsSenderApp().run()