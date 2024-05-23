from kivymd.uix.screen import MDScreen
from kivy.uix.screenmanager import SlideTransition
from kivymd.uix.button import MDRectangleFlatButton
from kivymd.uix.dialog import MDDialog
from kivy.storage.jsonstore import JsonStore
from kivy.clock import Clock

class Login(MDScreen):
    def on_enter(self, *args):
        Clock.schedule_once(self.CheckLogin)
        # start_detecting()

    def CheckLogin(self, *args):
        
        if(JsonStore("GUI//user.json").exists("User")):
            print("Already Logged In")
            self.manager.current = "MainScreen"
            
    
    dialog = None
    def neat_dialog(self,obj):
        self.dialog.dismiss()
		
  
  
    def show_alert_dialog(self):
        # app = MDApp.get_running_app()
        if not self.dialog:
            self.dialog = MDDialog(
                title = "Invalide Phone Number!",
                text = "Please Enter The Correct Phone Number...",
                buttons =[
                    MDRectangleFlatButton(
                        text="Ok", on_release = self.neat_dialog
                        ),
                    ],
                )

        self.dialog.open()
                
    def loginText(self):
        # pass
        textscratch = self.manager.get_screen('LoginScreen').ids.data.text
        text = textscratch.strip()
        
        try: 
            if(len(text) != 10):
                int("k")
            t = int(text)
            
        except Exception as ex:
            
            
            self.show_alert_dialog()
            
            
        else:
            
            store = JsonStore("GUI//user.json")
            store.put("User",name=text)
            
            self.manager.transition = SlideTransition(direction="left")
            
            self.manager.current = "MainScreen"
         