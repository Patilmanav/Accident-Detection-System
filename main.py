from kivy.lang import Builder
from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager
from kivy.utils import platform
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDRectangleFlatButton
from jnius import autoclass

from GUI.src.Classes.MainScreen import Main      
from GUI.src.Classes.LoginScreen import Login
from GUI.src.Classes.AccidentScreen import Accident
from GUI.src.Classes.Screen1 import Screen1
from GUI.src.Classes.Permission import GetPermission

import os

class MyApp(MDApp):
    dialog = None
    @staticmethod
    def start_service():
        service = autoclass("com.example.accidentdetection.ServiceAccidentdetection")
        mActivity = autoclass("org.kivy.android.PythonActivity").mActivity
        service.start(mActivity, "")
        
        # def stop_service():
        #     print("Hello")
        #     # service.stop(mActivity)
            
        return service
    
    def on_pause(self):
        print("App Paused!!")
        sm = self.root
        ActiveScreen = sm.current
        print(ActiveScreen)
        if ActiveScreen == 'Accident':
            from kivy import platform
            if platform == "android":
                try:
                    self.start_service()
                    print("service Started........")
                    
                except Exception as ex:
                    print(ex)
            else:
                print("Error While Starting Sevices")
            
        return True
    
    def on_resume(self):
        # return super().on_resume()
        print("App Resumed and Service is Stoped......")
        self.CheckServiceAvaiable()
        # self.stop_service()
        return True
    
    def on_start(self):
        # return super().on_start()
        self.CheckServiceAvaiable()
        
    def CheckServiceAvaiable(self):
        mActivity = autoclass("org.kivy.android.PythonActivity").mActivity
        path = mActivity.getFilesDir().getAbsolutePath() + "/app/CheckService.txt"
        if os.path.exists(path):
            self.show_alert_dialog()
    
    def DontStop(self,dt):
        if self.dialog:
            self.dialog.dismiss()
            
    def StopService(self,dt):
        mActivity = autoclass("org.kivy.android.PythonActivity").mActivity
        path = mActivity.getFilesDir().getAbsolutePath() + "/app/CheckService.txt"
        if self.dialog:
            self.dialog.dismiss()
            
        os.remove(path)
        self.stop_service()
        
        
    def show_alert_dialog(self):
        # app = MDApp.get_running_app()
        # self.dialog = None
        
        if not self.dialog:
            self.dialog = MDDialog(
                title = "Background Service is running!!",
                text = "Do you want to stop it .......",
                buttons =[
                    MDRectangleFlatButton(
                        text="No", on_release = self.DontStop
                        ),
                    MDRectangleFlatButton(
                        text="Yes", on_release = self.StopService
                        ),
                    ],
                auto_dismiss = False

                )
            self.dialog.open()
            
    @staticmethod
    def stop_service():
        # if not self.dialog:
        print("Hi")
        from jnius import autoclass
        service = autoclass("com.example.accidentdetection.ServiceAccidentdetection")
        mActivity = autoclass("org.kivy.android.PythonActivity").mActivity
        service.stop(mActivity)
             
    def build(self):
        if platform == "android":
            print("main.py: Android detected. Requesting permissions")
            GetPermission().request_android_permissions()
            
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Blue"
        
        
        # Load the KV files
        Builder.load_file('GUI//src//kvFiles//Login.kv')
        Builder.load_file('Main.kv')
        Builder.load_file('GUI//src//kvFiles//screen1.kv')
        Builder.load_file('GUI//src//kvFiles//Accident.kv')

        # Create a ScreenManager
        sm = ScreenManager()

        # Add screens to the ScreenManager
        sm.add_widget(Login(name='LoginScreen'))
        sm.add_widget(Main(name='MainScreen'))
        sm.add_widget(Screen1(name='screen1'))
        sm.add_widget(Accident(name='Accident'))

        return sm

if __name__ == '__main__':
    MyApp().run()
