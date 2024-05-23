from kivymd.uix.screen import MDScreen
from kivy.uix.screenmanager import SlideTransition
from kivy.clock import Clock
import math
from plyer import accelerometer
from kivymd.uix.button import MDRectangleFlatButton
from kivymd.uix.dialog import MDDialog
from GUI.src.Classes.GpslocSender import Send_SMS
from GUI.src.Classes import Jfunction
from kivy.properties import ObjectProperty
from plyer import vibrator

class Accident(MDScreen):
    alarm = None
    
    event = None
    dialog = None
    auto_call = None

            
    def not_detected(self,obj):
        if self.dialog:
            self.dialog.dismiss()
            
        if self.auto_call:
            Clock.unschedule(self.auto_call)
            
        print("Dialog No Button Clicked!!")
        # try:
        #     Jfunction.NotificationHandler(1).CancelNotification()
        # except Exception as ex:
        #     print(ex)
        if self.alarm:
            self.alarm.stop_alarm()
        vibrator.cancel()
        self.start_detecting()
        self.dialog = None
  
    def detected(self,obj):
        try:
            print("Dialog Yes Button Clicked!!")
            if self.dialog:
                self.dialog.dismiss()
            if self.auto_call:
                Clock.unschedule(self.auto_call)
            
            self.stop_detecting()
            
            
            Send_SMS().Start()
            try:
                Jfunction.NotificationHandler(0).ShowNotification("SMS Sended!!","SMS is Sended to the Emergency Contacts")
            except Exception as ex:
                print(ex)
                
            Clock.unschedule(self.event)
            # Clock.unschedule(self.detected)
            
        except Exception:
            import traceback
            traceback.print_exc()
            
        else:
            self.back_click()

    def stop_detecting(self):
        if self.dialog:
            self.dialog=None
            
        
        if self.alarm:
            self.alarm.stop_alarm()
        vibrator.cancel()
        # try:
        #     Jfunction.NotificationHandler(1).CancelNotification()
        # except Exception as ex:
        #     print(ex)
        # Jfunction.ToastText("Stopped Detecting!!")

        self.back_click()
        
    
    def start_detecting(self):
        accelerometer.enable()
        # Jfunction.ToastText("Started Detecting!!")
    
    def play_alarm(self):
        self.alarm = Jfunction.AlarmManager()
      
    def autoDetected(self,obj):
        if self.dialog:
            self.dialog.dismiss()
            
        self.stop_detecting()
        # try:
        #     Jfunction.NotificationHandler(1).CancelNotification()
        # except Exception as ex:
        #     print(ex)
        print("It is auto called!!")
        Clock.unschedule(self.event)
        Send_SMS().Start()
        try:
            Jfunction.NotificationHandler(0).ShowNotification("SMS Sended!!","SMS is Sended to the Emergency Contacts")
        except Exception as ex:
            print(ex)
        
        
    def show_alert_dialog(self):
        # app = MDApp.get_running_app()
        # self.dialog = None
        
        if not self.dialog:
            self.dialog = MDDialog(
                title = "Accident Detected!",
                text = "Please Confirm...",
                buttons =[
                    MDRectangleFlatButton(
                        text="No", on_release = self.not_detected
                        ),
                    MDRectangleFlatButton(
                        text="Yes", on_release = self.detected
                        ),
                    ],
                auto_dismiss = False

                )
            self.dialog.open()
            self.auto_call = Clock.schedule_once(self.autoDetected, 30)

    def on_leave(self, *args):
        # return super().on_leave(*args)
        print("Hi")    
    def on_pre_enter(self, *args):
        try:
            # self.dialog = None
            print("Hello")
            self.start_detecting()
            self.event = Clock.schedule_interval(self.get_acceleration, 1 / 20.)
            
        except NotImplementedError:
            import traceback
            traceback.print_exc()
            
        
        # return super().on_pre_enter(*args)
    def get_acceleration(self, dt):
        SHAKE_THRESHOLD = 50
        val = accelerometer.acceleration[:3]
        
        def magnitude(acceleration):
            
            return math.sqrt(sum(float(a)**2 for a in acceleration))
        if not val == (None, None, None):
            
            accel_magnitude = magnitude(val)
            if accel_magnitude > float(SHAKE_THRESHOLD):
                print("Shake detected!")
                accelerometer.disable()
                self.show_alert_dialog()
                self.play_alarm()
                if vibrator.exists():
                    l1 = [0,2,2,2,2,5,2,3,2,3,2,9]  
                    vibrator.pattern(float(n) for n in l1)
                # try:
                #     Jfunction.NotificationHandler(1).ShowNotification(Title="Accident Detected",Text="Please Confirm within 30 sec.....",AutoCancel=True,Ongoing=True)
                # except Exception as ex:
                #     print(ex)
                
     
    def back_click(self):
        self.manager.transition = SlideTransition(direction="right")
        self.manager.current = "MainScreen"
