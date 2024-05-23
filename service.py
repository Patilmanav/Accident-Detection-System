from plyer import accelerometer,vibrator
import math
import threading
from GUI.src.Classes import Jfunction
# import notificatonaction as notify
from jnius import autoclass, cast
from android.runnable import run_on_ui_thread
from GUI.src.Classes.GpslocSender import Send_SMS

# Gets the current running instance of the app so as to speak
from os import environ
from jnius import autoclass
import os

mService = autoclass("org.kivy.android.PythonService").mService
path = mService.getFilesDir().getAbsolutePath() + "/app/CheckService.txt"
if not os.path.exists(path):
    f=open(path,'w')
    f.write("Background Service")
    

ANDROID_VERSION = autoclass('android.os.Build$VERSION')
SDK_INT = ANDROID_VERSION.SDK_INT
global PythonActivity
global PythonService
global activity

# acc_detected = None
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
    
    
print("SErvice.PY")
LocationService = autoclass("org.org.example.LocationService")

context = activity.getApplicationContext()


NotiBtnClicked = None
alarm = None
event=None

# context = activity.getApplicationContext()

# Autoclass necessary java classes so they can be used in python
RingtoneManager = autoclass("android.media.RingtoneManager")
Uri = autoclass("android.net.Uri")
AudioAttributesBuilder = autoclass("android.media.AudioAttributes$Builder")
AudioAttributes = autoclass("android.media.AudioAttributes")
AndroidString = autoclass("java.lang.String")
NotificationManager = autoclass("android.app.NotificationManager")
NotificationChannel = autoclass("android.app.NotificationChannel")
NotificationCompat = autoclass("androidx.core.app.NotificationCompat")
NotificationCompatActionBuilder = autoclass("androidx.core.app.NotificationCompat$Action$Builder")
NotificationCompatBuilder = autoclass("androidx.core.app.NotificationCompat$Builder")
NotificationManagerCompat = autoclass("androidx.core.app.NotificationManagerCompat")
func_from = getattr(NotificationManagerCompat, "from")
Intent = autoclass("android.content.Intent")
PendingIntent = autoclass("android.app.PendingIntent")
Context = autoclass("android.content.Context")
# Autoclass our own java class
action1 = autoclass("org.org.example.Action1")
action2 = autoclass("org.org.example.Action2")
# from src.Action1 import Action1

# # Instantiate your BroadcastReceiver class or function
# action1 = Action1()


def create_channel(c_id="Channel1"):
    # create an object that represents the sound type of the notification
    sound = cast(Uri, RingtoneManager.getDefaultUri(RingtoneManager.TYPE_NOTIFICATION))
    att = AudioAttributesBuilder()
    att.setUsage(AudioAttributes.USAGE_NOTIFICATION)
    att.setContentType(AudioAttributes.CONTENT_TYPE_SONIFICATION)
    att = cast(AudioAttributes, att.build())

    # Name of the notification channel
    name = cast("java.lang.CharSequence", AndroidString("Channel Name"))
    # Description for the notification channel
    description = AndroidString("Channel Description")
    # Unique id for a notification channel. Is used to send notification through
    # this channel
    global channel_id
    channel_id = AndroidString(c_id)

    # Importance level of the channel
    importance = NotificationManager.IMPORTANCE_HIGH
    # Create Notification Channel
    channel = NotificationChannel(channel_id, name, importance)
    channel.setDescription(description)
    channel.enableLights(True)
    channel.enableVibration(True)
    channel.setSound(sound, att)
    # Get android's notification manager
    notificationManager = context.getSystemService(NotificationManager)
    # Register the notification channel
    notificationManager.createNotificationChannel(channel)


def create_notification(ContentTitle,ContentText,NotiId):
    # Set notification sound
    sound = cast(Uri, RingtoneManager.getDefaultUri(RingtoneManager.TYPE_NOTIFICATION))
    # Create the notification builder object
    builder = NotificationCompatBuilder(context, channel_id)
    # Sets the small icon of the notification
    global mip_icon
    mip_icon = context.getApplicationInfo().icon
    print(mip_icon)
    builder.setSmallIcon(mip_icon)
    # Sets the title of the notification
    builder.setContentTitle(
        cast("java.lang.CharSequence", AndroidString(ContentTitle)) #"Accident Detected!!"
    )
    # Set text of notification
    builder.setContentText(
        cast("java.lang.CharSequence", AndroidString(ContentText)) #"Press No in case of False detection.."
    )
    # Set sound
    builder.setSound(sound)
    # Set priority level of notification
    builder.setPriority(NotificationCompat.PRIORITY_HIGH)
    # If notification is visble to all users on lockscreen
    builder.setVisibility(NotificationCompat.VISIBILITY_PUBLIC)
    builder.setAutoCancel(False)
    builder.setOngoing(True)
    intentClass = None
    textString = None
    if NotiId==0:
        intentClass = action2
        textString = "Stop Service"
    elif NotiId==8520:
        intentClass = action1
        textString = "No"
    # code to add an action button
    # Creating intent with our own java class
    intent = Intent(context, intentClass)
    intent.putExtra("NOTIFID",0)
    intent.putExtra("LAUNCHED_FROM_NOTIF", 0)
    
    # Creating our PendingIntent
    pendingintent = PendingIntent.getBroadcast(
        context, 1, intent, PendingIntent.FLAG_MUTABLE
    )
    # Create the action object
    # Give it an id and a string to represent the text to be shown on the notification
    a = cast('java.lang.CharSequence', AndroidString(textString))
    
    # ________ICON_______________
    global activity
    # Mipmap = autoclass("{}.R$mipmap".format(activity.getPackageName()))
    # icon = Mipmap.icon
    try:
        icon = mip_icon
        print("mipmap icon")
        # action1_button = NotificationCompatActionBuilder(
        # icon, a, pendingintent
        # ).build()
        # # Add the action to the notification
        # builder.addAction(action1_button)
    except Exception as ex:
        icon = 0
        print(ex)
            

    action1_button = NotificationCompatActionBuilder(
        icon, a, pendingintent
    ).build()
    # Add the action to the notification
    builder.addAction(action1_button)

    # Create a notificationcompat manager object to add the new notification
    compatmanager = func_from(context)
    # Pass an unique notification_id. This can be used to access the notification
    compatmanager.notify(NotiId, builder.build())
    

def Notify(ContentTitle,ContentText,NotiId,c_id = "Channel1"):
    global activity
    global event
    global NotiBtnClicked
    try:
        create_channel(c_id)
        create_notification(ContentTitle,ContentText,NotiId)
        if NotiId == 0:
            start_detecting()

    except Exception as ex:
        print(ex)
    else:
        if NotiId == 8520:
            print("Notification Send")
            import time
            endloop = time.time() + 30
            j=0
            while time.time() < endloop:
                NotiBtnClicked = None
                print(time.time())
                NotificationManager = autoclass('android.app.NotificationManager')
            
                notification_manager = activity.getSystemService(activity.NOTIFICATION_SERVICE)

                active_notifications = notification_manager.getActiveNotifications()
                for notification in active_notifications:
                    if notification.getId() != 0:
                        # print(notification.getId())
                        if notification.getId() == 8520:
                            print("Notification Action Button Not Triggered Yet!!")
                            NotiBtnClicked = True
                            break
                        # elif notification.getId() != 8520:
                        #     print("Action button Clicked!!")
                        #     NotiBtnClicked = True
                        
                if not NotiBtnClicked:
                    break    
                # if not active_notifications:
                    
                #     # NotiBtnClicked = True
                #     print("No Active Notifications......")
                     
                # else:
                #     print("active_notifications are ",active_notifications)
                    
            if not NotiBtnClicked:
                print("Button Clicked......")
                vibrator.cancel()
                if alarm:
                    alarm.stop_alarm()
                start_detecting()
            
            else:
                vibrator.cancel()
                if alarm:
                    alarm.stop_alarm()
                event.cancel()
                # Send_SMS().Start()
                compatmanager = func_from(context)

                compatmanager.cancel(8520)
                compatmanager.cancel(0)
                Intent = autoclass("android.content.Intent")
                serviceIntent = Intent(activity.getApplicationContext(), LocationService)

                # // Start the service
                activity.getApplicationContext().startService(serviceIntent)
                print("MyApp: ","Service Started")
            
        # else:
        #     print(NotiId)
        #     print("Service Started!!")
            
def isNotiBtnClicked():
    return NotiBtnClicked
import time
def get_acceleration():
    while True:
        # global acc_detected
        # acc_detected = False
        global event
        SHAKE_THRESHOLD = 50
        val = accelerometer.acceleration[:3]
        print(val)
        print("--------------accelerometer on------------------")
        def magnitude(acceleration):
            return math.sqrt(sum(float(a)**2 for a in acceleration))
        
        if not val == (None, None, None):
            
            accel_magnitude = magnitude(val)
            if accel_magnitude > float(SHAKE_THRESHOLD):
                accelerometer.disable()
                # event.()
                print("Shake detected!")
                # acc_detected = True
                global alarm
                if vibrator.exists():
                    l1 = [0,2,2,2,2,5,2,3,2,3,2,9]  
                    vibrator.pattern(float(n) for n in l1)
                print("Vibrating...")
                alarm = Jfunction.AlarmManager()
                print("Alarm Started")
                ContentTitle = "Accident Detected!!"
                ContentText = "Press No in case of False detection.."
                NotiId = 8520
                c_id = "Channel6"
                Notify(ContentTitle,ContentText,NotiId,c_id)
                print("Notification Send")
                break
        time.sleep(1 / 20)
                
            
    # event = threading.Timer(1 / 20. ,get_acceleration)
    # event.start()
    
    # if acc_detected:
    #     event.cancel()
    
            
            
    
def start_detecting():
    try:
        global event
        # self.dialog = None
        print("Accelerometer Started.......")
        accelerometer.enable()
        event = threading.Timer(1 / 20. ,get_acceleration)
        event.start()
        
    except NotImplementedError:
        import traceback
        traceback.print_exc()
    


print("Service file")
ContentTitle = "Accident Detection Started"
ContentText = "Background process is running..."
NotiId = 0
Notify(ContentTitle,ContentText,NotiId)


# Intent = autoclass("android.content.Intent")
# serviceIntent = Intent(activity, LocationService)

# # // Start the service
# activity.getApplicationContext().startService(serviceIntent)
# print("MyApp: ","Service Started")