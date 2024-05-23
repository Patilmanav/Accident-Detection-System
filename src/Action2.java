package org.org.example;
//The package name of your android app

import androidx.core.app.NotificationManagerCompat;
import android.content.BroadcastReceiver;
import android.content.Intent;
import android.content.Context;
import android.app.Service;
import java.io.File;
import android.util.Log;
import android.widget.Toast;
import org.kivy.android.PythonService;
import com.example.accidentdetection.ServiceAccidentdetection;
public class Action2 extends BroadcastReceiver{

  @Override
  public void onReceive(Context context, Intent intent) {
      // Code to execute once the button has been pressed
        NotificationManagerCompat notificationManager = NotificationManagerCompat.from(context);
        notificationManager.cancel(0);
        
        // PythonService.mService.stopService(new Intent( PythonService.mService, ServiceAccidentdetection.class ) ); 
        try{
          Intent intent2 = new Intent(context, ServiceAccidentdetection.class);
          context.stopService(intent2);
        }
        catch(Exception ex){
          String e = ex.toString();
          Log.d("Service Error",e);
          context.stopSelf(1);
        }

        String path = context.getFilesDir().getAbsolutePath() + "/app/CheckService.txt";
        File f = new File(path);
        if(f.isFile() && f.exists()){
          Log.d("MyApp","File is present\nMeans Service is running\nDestroying it!!");
          f.delete();

        }
        
        System.out.println("BG service Stoped!!");
        Toast.makeText(context,"BG service Stoped",Toast.LENGTH_SHORT).show();  

    }
   
}