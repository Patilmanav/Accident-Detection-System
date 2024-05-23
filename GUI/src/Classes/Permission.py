from kivy.clock import mainthread
from kivy.utils import platform



class GetPermission():


    def request_android_permissions(self):
        """
        Since API 23, Android requires permission to be requested at runtime.
        This function requests permission and handles the response via a
        callback.

        The request will produce a popup if permissions have not already been
        been granted, otherwise it will do nothing.
        """
        from android.permissions import request_permissions, Permission

        def callback(permissions, results):
            """
            Defines the callback to be fired when runtime permission
            has been granted or denied. This is not strictly required,
            but added for the sake of completeness.
            """
            if all([res for res in results]):
                print("callback. All permissions granted.")
            else:
                print("callback. Some permissions refused.")
                
                

        request_permissions([Permission.ACCESS_COARSE_LOCATION,
                             Permission.ACCESS_FINE_LOCATION,
                             Permission.INTERNET,
                             Permission.SEND_SMS,
                             Permission.READ_CONTACTS,
                             Permission.POST_NOTIFICATIONS,
                             Permission.ACCESS_BACKGROUND_LOCATION,
                             Permission.REQUEST_IGNORE_BATTERY_OPTIMIZATIONS], callback)
        # # To request permissions without a callback, do:
        # request_permissions([Permission.ACCESS_COARSE_LOCATION,
        #                      Permission.ACCESS_FINE_LOCATION])



