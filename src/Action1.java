package org.org.example;
//The package name of your android app

import androidx.core.app.NotificationManagerCompat;
import android.content.BroadcastReceiver;
import android.content.Intent;
import android.content.Context;
import android.widget.Toast;
import org.kivy.android.PythonService;

public class Action1 extends BroadcastReceiver{

  @Override
  public void onReceive(Context context, Intent intent) {
      // Code to execute once the button has been pressed
        NotificationManagerCompat notificationManager = NotificationManagerCompat.from(context);
        notificationManager.cancel(8520);
        System.out.println("Action Button Clicked!!");
        Toast.makeText(context,"Action Button Clicked!!",Toast.LENGTH_SHORT).show();  

    }
}