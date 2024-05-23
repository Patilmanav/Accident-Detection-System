from kivymd.uix.screen import MDScreen
from kivy.uix.screenmanager import SlideTransition
from kivy.storage.jsonstore import JsonStore

import sqlite3 as sql


class Main(MDScreen):
    def on_enter(self, *args):
        self.ids.nav_header.text = self.manager.get_screen('LoginScreen').ids.data.text
        
        
    def openGpsSettings(self):
        from jnius import autoclass

        # Get the necessary classes
        Settings = autoclass('android.provider.Settings')
        Intent = autoclass('android.content.Intent')
        Context = autoclass('android.content.Context')
        PythonActivity = autoclass('org.kivy.android.PythonActivity').mActivity

        # Get the application context
        app_context = PythonActivity.getApplicationContext()

        # Open the settings screen with FLAG_ACTIVITY_NEW_TASK flag
        intent = Intent(Settings.ACTION_LOCATION_SOURCE_SETTINGS)
        intent.addFlags(Intent.FLAG_ACTIVITY_NEW_TASK)
        app_context.startActivity(intent)
    
    def isGPSEnabled(self):
        from jnius import autoclass

        # Get the necessary classes
        Context = autoclass('android.content.Context')
        LocationManager = autoclass('android.location.LocationManager')
        PythonActivity = autoclass('org.kivy.android.PythonActivity').mActivity

        # Get the context
        context = PythonActivity.getApplicationContext()

        # Get the location manager
        location_manager = context.getSystemService(Context.LOCATION_SERVICE)

        # Check if GPS provider is enabled
        is_gps_enabled = location_manager.isProviderEnabled(LocationManager.GPS_PROVIDER)

        if is_gps_enabled:
            print("GPS is enabled")
            return True
        else:
            print("GPS is not enabled")
            return False
            
        
    def CheckAccident(self):
        con=sql.connect('Emergency_contacts.db')
        cur=con.cursor()
        print("Hi")
        cur.execute('''SELECT name FROM sqlite_master WHERE type='table' AND name='contact' ''')
        d = cur.fetchall()

        if self.isGPSEnabled():
            if len(d)<1:
                from GUI.src.Classes import Jfunction
                Jfunction.ToastText("Please add atleast one contact before Start!!")
                self.manager.transition = SlideTransition(direction="left")
                self.manager.current = "screen1"
            else:
                # Jfunction.ToastText("BackGround Service Started")
                self.manager.transition = SlideTransition(direction="left")
                self.manager.current = "Accident"
            
        else:
            print("Turn On GPS...")
            from GUI.src.Classes import Jfunction
            Jfunction.ToastText("Please turn on the Location before Start!!")
            self.openGpsSettings()
        
        
    def logout(self):
        JsonStore("GUI//user.json").delete("User")
        print("LogOut")
        self.ids.nav_drawer.set_state("close")
        self.manager.transition = SlideTransition()
        self.manager.current = "LoginScreen"
        
    def Contacts(self):
        self.ids.nav_drawer.set_state("close")
        self.manager.transition = SlideTransition(direction="left")
        self.manager.current = "screen1"
    
    # @staticmethod
    # def start_service():
    #     from jnius import autoclass
    #     service = autoclass("com.example.accidentdetection.ServiceAccidentdetection")
    #     mActivity = autoclass("org.kivy.android.PythonActivity").mActivity
    #     service.start(mActivity, "")
        
    #     # def stop_service():
    #     #     print("Hello")
    #     #     # service.stop(mActivity)
            
    #     return service