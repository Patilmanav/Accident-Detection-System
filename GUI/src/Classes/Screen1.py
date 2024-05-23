from kivymd.uix.screen import MDScreen
from kivy.uix.screenmanager import SlideTransition
from kivymd.uix.list import TwoLineAvatarIconListItem,IconRightWidget
from jnius import cast,autoclass
from kivy.clock import Clock
from android.runnable import run_on_ui_thread
from android import activity
import sqlite3 as sql
from kivy.core.window import Window
from kivy.properties import ObjectProperty
from GUI.src.Classes import Jfunction
import os

con=sql.connect('Emergency_contacts.db')
cur=con.cursor()
        
class Screen1(MDScreen):
    
    def __init__(self,**kwargs):
        super(Screen1,self).__init__(**kwargs)
        # code goes here and add:
        
        self.list_items=[]
    
    def on_pre_enter(self,*kwargs):
        Window.bind(on_keyboard=self.hook_keyboard)
        self.update_list()
        
    def update_list(self):
        cur.execute('''SELECT name FROM sqlite_master WHERE type='table' AND name='contact' ''')
        d = cur.fetchall()
        
        cur.execute("select * from contact")
        rows = cur.fetchall()
            
        if len(d) < 1 or len(rows) <= 0:
            self.ids.container.clear_widgets()
            print("No contact in the List")
            item = TwoLineAvatarIconListItem(
                    text="No Contact Added yet!!",
                    secondary_text= "Please add atleast one.....",
                )
            self.list_items.append(item)
            self.ids.container.add_widget(item)
            
        elif len(d)==1:
            self.list_items=[]
            self.ids.container.clear_widgets()
            # cur.execute("select * from contact")
            # rows = cur.fetchall()
                

            item = None
            i=0
            
            for row in rows:
                name = row[0]
                phone = row[1]
                
                item = TwoLineAvatarIconListItem(
                    
                    IconRightWidget(
                        icon="trash-can",
                        on_press=(lambda x, i=i: self.remove_contact(i))
                    ),
                    
                    text=name,
                    secondary_text= phone,
                )
                self.list_items.append(item)
                self.ids.container.add_widget(item)
                i+=1
                
    def remove_contact(self,index):
        print("Removing Contact......",self.list_items[index].text)
        cur.execute(f"DELETE FROM contact WHERE name = '{self.list_items[index].text}' ")
        con.commit()
        Jfunction.ToastText("Contact Removed!!")
        self.update_list()
        
        
        
    def hook_keyboard(self, window, key, *largs):
        if key == 27:
        # do what you want, return True for stopping the propagation
            self.manager.transition = SlideTransition(direction="right")
            self.manager.current = 'MainScreen'
            return True 

    
 
    def store_contact(self,contact):
        cur.execute('''SELECT name FROM sqlite_master WHERE type='table' AND name='contact' ''')

        d = cur.fetchall()
        if len(d) < 1:
            # Table not Found Creating new
            cur.execute('''
                    create table contact(
                        
                        name text(100),
                        phone text(100)
                    )
                    ''')
            con.commit()
        
        for i,j in contact.items():
            cur.execute(f"insert into contact(name,phone) values('{i}','{j}')")
            print("Contact Added In Database!!")
            con.commit()
            Jfunction.ToastText(f"Contact {j} Added!!")
        self.update_list()
            
    def pick_contact(self):
        print("pick")
        
        
        PythonActivity = autoclass('org.kivy.android.PythonActivity')
        currentActivity = PythonActivity.mActivity
        Intent = autoclass('android.content.Intent')
        ContactsContract = autoclass('android.provider.ContactsContract$Contacts')
        ContentUris = autoclass('android.content.ContentUris')
        ContentResolver = autoclass('android.content.ContentResolver')
        Cursor = autoclass('android.database.Cursor')
        Uri = autoclass('android.net.Uri')
        
        
        
        def open_contacts():
            intent = Intent()
            intent.setAction(Intent.ACTION_PICK)
            intent.setType(ContactsContract.CONTENT_TYPE)
            
            # Start activity for result 
            activity.bind(on_activity_result=show_result) 
            PythonActivity.mActivity.startActivityForResult(intent, 0)
            
        global first_pick    
        first_pick = True
        def show_result(requestCode, resultCode, intent):
            if requestCode == 0:
                if resultCode == PythonActivity.RESULT_OK:
                    # Get contact URI
                    uri = intent.getData()
                    Phone = autoclass('android.provider.ContactsContract$CommonDataKinds$Phone')
                    try:
                        # Define projection (columns to fetch)
                        # projection = ['display_name',Phone.NUMBER]
                        
                        # Query Contacts Provider
                        cursor = currentActivity.getContentResolver().query(uri, None, None, None, None)
                        # verifing.....................
                        # print("name and Contact: ",cursor.getColumnNames())
                    except Exception as ex:
                        print(ex)
                        print("ExceptionHandled: phonenumber is incorrect, so using number instead")
                        
                    #if 
                    if cursor.moveToFirst():
                        name_index = cursor.getColumnIndex(ContactsContract.DISPLAY_NAME)
                        number_index = cursor.getColumnIndex(ContactsContract._ID)
                        name = cursor.getString(name_index)
                        contact_id = cursor.getString(number_index)
                        phone_uri = Phone.CONTENT_URI
                        cursor = currentActivity.getContentResolver().query(phone_uri, None,
                                                                    Phone.CONTACT_ID
                                                                    + " = ?", [contact_id], None)
                        if cursor.moveToFirst():
                            phone_index = cursor.getColumnIndex(Phone.NUMBER)
                            phone_number = cursor.getString(phone_index)
                            result = {"name": name, "phone": phone_number}
                            # print('result: ',result)
                            contact = {name : phone_number}
                            
                        global first_pick
                        if first_pick:
                            
                            print("Show_resilt = ",contact)
                            try:
                                Clock.schedule_once(lambda dt: self.store_contact(contact), 0)
                            except Exception as ex:
                                print("run-thread",ex)
                            
                            
                        
                    cursor.close
            # global first_pick
            first_pick = False     
                        
        # Trigger contact picker  
        open_contacts()
        
            
    def back_click(self):
        # print("Back Button")
        self.manager.transition = SlideTransition(direction="right")
        self.manager.current = 'MainScreen'