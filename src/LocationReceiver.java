package org.org.example;

import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.Intent;
import android.os.Bundle;
import android.util.Log;
import android.telephony.SmsManager;
import android.widget.Toast;
import android.database.Cursor;
import android.database.sqlite.SQLiteDatabase;
// import android.os.Environment;

public class LocationReceiver extends BroadcastReceiver {
    private DatabaseManager databaseManager;
    @Override
    public void onReceive(Context context, Intent intent) {
        // Toast.makeText( context.getApplicationContext(), "Hello from Reciever", Toast.LENGTH_SHORT ).show();
        Bundle extras = intent.getExtras();
        if (extras != null) {
            Log.d("LocationReceiver", "Received location update");
            Log.d("Latitude", ":" + extras.getString("Latitude"));
            Log.d("Longitude", ":" + extras.getString("Longitude"));
            Log.d("Provider", ":" + extras.getString("Provider"));
            // Environment.getDataDirectory().getAbsolutePath();
            // Toast.makeText( context, "Location Recieved", Toast.LENGTH_SHORT ).show();

            // String path = context.getFilesDir().getAbsolutePath();
            // Create an instance of DatabaseManager passing the context (this)
            databaseManager = new DatabaseManager(context);
            Cursor cursor = databaseManager.getDataFromDatabase();

            getData(cursor,extras.getString("Latitude"),extras.getString("Longitude"),context);
            
        }
    }

    private void getData(Cursor cursor,String lat,String lon,Context context){
        if (cursor != null && cursor.moveToFirst()) {
            do {
                // Assuming the "name" column exists in your_table
                String name = cursor.getString(cursor.getColumnIndex("name"));
                String phone = cursor.getString(cursor.getColumnIndex("phone"));
                String message = String.format("https://maps.google.com/?q=%s,%s",lat,lon);
                String final_message = String.format("I Need Your Help ! \nI have had an accident \nPlease take me from : %s",message);
                Log.d("MyApp","Name = "+name);
                Log.d("MyApp","Phone = "+phone);
                // Toast.makeText( context, name+"\n"+phone, Toast.LENGTH_SHORT ).show();
                
                String[] ph = phone.split(",");
                Log.d("MyApp","Ph = "+ph);

                try {
                    SmsManager smsManager = SmsManager.getDefault();
                    smsManager.sendTextMessage(ph[0], null, final_message, null, null);
                    // Toast.makeText(context, "SMS sent successfully", Toast.LENGTH_SHORT).show();
                    Log.d("MyApp","SMS sent successfully");
                } catch (Exception e) {
                    // Toast.makeText(context, "SMS sending failed", Toast.LENGTH_SHORT).show();
                    e.printStackTrace();
                    Log.d("MyApp","SMS sending failed");

                }

            } while (cursor.moveToNext());
            cursor.close();
        }
    }
}

class DatabaseManager {
    private SQLiteDatabase database;

    public DatabaseManager(Context context) {
        // Assuming context is passed from your activity or application
        String dbPath = context.getFilesDir().getAbsolutePath() + "/app/Emergency_contacts.db"; // Full path to your database file
        database = SQLiteDatabase.openDatabase(dbPath, null, SQLiteDatabase.OPEN_READWRITE);
    }

    public Cursor getDataFromDatabase() {
        Cursor cursor = database.rawQuery("SELECT * FROM contact", null);
        // You can now use the cursor to read data from the database
        return cursor;
    }

    public void closeDatabase() {
        if (database != null && database.isOpen()) {
            database.close();
        }
    }
}