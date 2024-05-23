from jnius import autoclass, cast
from android import python_act
from kvdroid.tools import get_resource


# Gets the current running instance of the app so as to speak
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
    
context = activity.getApplicationContext()

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


def create_notification(ContentTitle,ContentText,NotiId=0,addAction = False):
    # Set notification sound
    sound = cast(Uri, RingtoneManager.getDefaultUri(RingtoneManager.TYPE_NOTIFICATION))
    # Create the notification builder object
    builder = NotificationCompatBuilder(context, channel_id)
    # Sets the small icon of the notification
    global mip_icon
    mip_icon = context.getApplicationInfo().icon
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
    if addAction:
        # code to add an action button
        # Creating intent with our own java class
        intent = Intent(context, action1)
        intent.putExtra("NOTIFID",0)
        intent.putExtra("LAUNCHED_FROM_NOTIF", 0)
        
        # Creating our PendingIntent
        pendingintent = PendingIntent.getBroadcast(
            context, 1, intent, PendingIntent.FLAG_MUTABLE
        )
        # Create the action object
        # Give it an id and a string to represent the text to be shown on the notification
        a = cast('java.lang.CharSequence', AndroidString('No'))
        
        # ________ICON_______________
        global activity
        # Mipmap = autoclass("{}.R$mipmap".format(activity.getPackageName()))
        # icon = Mipmap.icon
        try:
            icon = mip_icon
            print("mipmap icon")
            action1_button = NotificationCompatActionBuilder(
            icon, a, pendingintent
            ).build()
            # Add the action to the notification
            builder.addAction(action1_button)
        except Exception as ex:
            print(ex)
            try:
                icon = get_resource("drawable").bell
                print("Bell icon")
                action1_button = NotificationCompatActionBuilder(
                icon, a, pendingintent
                ).build()
                # Add the action to the notification
                builder.addAction(action1_button)
            except Exception as e:
                print(e)
                icon = 0
                print("int 0")
                action1_button = NotificationCompatActionBuilder(
                icon, a, pendingintent
                ).build()
                # Add the action to the notification
                builder.addAction(action1_button)
            

        # action1_button = NotificationCompatActionBuilder(
        #     icon, a, pendingintent
        # ).build()
        # # Add the action to the notification
        # builder.addAction(action1_button)

    # Create a notificationcompat manager object to add the new notification
    compatmanager = func_from(context)
    # Pass an unique notification_id. This can be used to access the notification
    compatmanager.notify(NotiId, builder.build())