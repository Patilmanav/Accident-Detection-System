class AlarmManager():
    media_player = None
    def __init__(self):
                
        from jnius import autoclass
        from os import environ
        from jnius import autoclass

        ANDROID_VERSION = autoclass('android.os.Build$VERSION')
        SDK_INT = ANDROID_VERSION.SDK_INT
        global PythonActivity
        try:
            from android import config
            ns = config.JAVA_NAMESPACE
        except (ImportError, AttributeError):
            ns = 'org.renpy.android'

        if 'PYTHON_SERVICE_ARGUMENT' in environ:
            self.PythonActivity = autoclass(ns + '.PythonService')
            self.activity = self.PythonActivity.mService
            context = self.activity.getApplicationContext()
        else:
            self.PythonActivity = autoclass(ns + '.PythonActivity')
            self.activity = self.PythonActivity.mActivity
            context = self.activity
    
        # def onCompletion():
        #     # self.media_player.prepare()
        #     self.media_player.start()

        # if start
        
        # Get the Android context
        # PythonActivity = autoclass('org.kivy.android.PythonActivity')
        # context = PythonActivity.mActivity

        # Get the audio manager
        AudioManager = autoclass('android.media.AudioManager')
        audio_manager = context.getSystemService(context.AUDIO_SERVICE)

        # Request audio focus for playback
        audio_focus_request = AudioManager.AUDIOFOCUS_GAIN
        audio_manager.requestAudioFocus(None, AudioManager.STREAM_ALARM, audio_focus_request)

        # Set the stream type to alarm and play the default alarm sound
        Media = autoclass('android.media.MediaPlayer')
        self.media_player = Media()
        self.media_player.setAudioStreamType(AudioManager.STREAM_ALARM)

        RingtoneManager = autoclass('android.media.RingtoneManager')
        default_alarm_uri = RingtoneManager.getDefaultUri(RingtoneManager.TYPE_ALARM)
        self.media_player.setDataSource(context, default_alarm_uri)

        self.media_player.prepare()
        self.media_player.start()
        # self.media_player.setOnCompletionListener(onCompletion())
        
        # Schedule the alarm sound to play at a certain time
        AlarmManager = autoclass('android.app.AlarmManager')
        alarm_manager = context.getSystemService(context.ALARM_SERVICE)

        Intent = autoclass('android.content.Intent')
        intent = Intent(context, self.PythonActivity)
        intent.setFlags(Intent.FLAG_ACTIVITY_NEW_TASK)

        PendingIntent = autoclass('android.app.PendingIntent')
        pending_intent = PendingIntent.getActivity(context, 0, intent, PendingIntent.FLAG_IMMUTABLE)
        
        System = autoclass('java.lang.System')
        
        Calendar = autoclass('java.util.Calendar')
        calendar = Calendar.getInstance()
        calendar.setTimeInMillis(System.currentTimeMillis())
        calendar.set(Calendar.HOUR_OF_DAY, 7)  # Set the alarm time (e.g., 7 AM)
        calendar.set(Calendar.MINUTE, 0)
        calendar.set(Calendar.SECOND, 0)

        alarm_manager.set(AlarmManager.RTC_WAKEUP, calendar.getTimeInMillis(), pending_intent)
        
        # return media_player
    def stop_alarm(self):
        if self.media_player:
            # self.media_player.prepare()
            self.media_player.stop()
            self.media_player.release()
            self.media_player = None
            
        else:
            print("Jfunction: MP is Null!!")


def ToastText(TexttoToast):
    try:
        
        from android import autoclass, cast
        from android.runnable import run_on_ui_thread
        Build = autoclass("android.os.Build")
        AndroidString = autoclass('java.lang.String')
        VERSION = autoclass("android.os.Build$VERSION")
        Device = Build.MANUFACTURER
        version = int(VERSION.RELEASE[:])
        Toast = autoclass('android.widget.Toast')
        activity = autoclass("org.kivy.android.PythonActivity").mActivity

        @run_on_ui_thread
        def toast():
            # global Toast, activity, cast, AndroidString, Device, version
            Toast.makeText(
                    activity,
                    cast('java.lang.CharSequence', AndroidString(TexttoToast)),
                    Toast.LENGTH_LONG
                ).show()
        toast()
        
    except Exception as ex:
        print(ex)

class NotificationHandler():
    
    def __init__(self,n_id=0):

        self.n_id = n_id
        
        
    
    notification_manager = None
    
    def CancelNotification(self):
        
        if self.notification_manager:
            self.notification_manager.cancel(self.n_id)
    
    def ShowNotification(self,Title,Text,AutoCancel=True,Ongoing=False):
        try:
            
            from jnius import autoclass

            # Get the Android context
            PythonActivity = autoclass('org.kivy.android.PythonActivity')
            context = PythonActivity.mActivity


            # Create a notification channel
            NotificationManager = autoclass('android.app.NotificationManager')
            self.notification_manager = context.getSystemService(context.NOTIFICATION_SERVICE)
            channel_id = "my_channel_id"
            channel_name = "My Channel"
            importance = NotificationManager.IMPORTANCE_DEFAULT
            channel = autoclass('android.app.NotificationChannel')(channel_id, channel_name, importance)
            self.notification_manager.createNotificationChannel(channel)

            # Create a notification builder
            Notification = autoclass('android.app.Notification')
            NotificationBuilder = autoclass('android.app.Notification$Builder')
            notification_builder = NotificationBuilder(context, channel_id)

            # Set notification properties
            notification_builder.setContentTitle(Title)
            notification_builder.setContentText(Text)
            notification_builder.setSmallIcon(context.getApplicationInfo().icon)
            notification_builder.setOngoing(Ongoing)
            notification_builder.setAutoCancel(AutoCancel)
            
            # Create a pending intent for the button
            Intent = autoclass('android.content.Intent')
            PendingIntent = autoclass('android.app.PendingIntent')
            intent = Intent(context, PythonActivity)
            intent.setFlags(Intent.FLAG_ACTIVITY_SINGLE_TOP)

            # Replace 1 with a unique integer value
            pending_intent = PendingIntent.getBroadcast(context, 1, intent, PendingIntent.FLAG_IMMUTABLE)

            # Build the notification and show it
            notification = notification_builder.build()
            self.notification_manager.notify(self.n_id, notification)
            
        except Exception as ex:
            print(ex)