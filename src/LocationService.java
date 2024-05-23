package org.org.example;

import android.app.Service;
import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.Intent;
import android.content.pm.PackageManager;
import android.location.Location;
import android.location.LocationListener;
import android.location.LocationManager;
import android.net.Uri;
import android.os.Bundle;
import android.os.IBinder;
import android.util.Log;
import android.widget.Toast;
import org.org.example.LocationReceiver;
import androidx.core.app.ActivityCompat;


public class LocationService extends Service {

    public static final String BROADCAST_ACTION = "BroadcastLocationFastium";
    private static final int TWO_MINUTES = 1000 * 60 * 2;
    private LocationManager locationManager;
    private MyLocationListener listener;
    private Location previousBestLocation = null;

    @Override
    public void onCreate() {
        super.onCreate();
        locationManager = (LocationManager) getSystemService(Context.LOCATION_SERVICE);
        listener = new MyLocationListener();
        Log.d("MyApp","Service Loc activated!!");
        // Toast.makeText( getApplicationContext(), "Hello from Service", Toast.LENGTH_SHORT ).show();

    }

    @Override
    public int onStartCommand(Intent intent, int flags, int startId) {
        
        Log.d("MyApp","StartCommand!!");
        // Toast.makeText( getApplicationContext(), "StartCommand!!", Toast.LENGTH_SHORT ).show();
        if (ActivityCompat.checkSelfPermission(this, android.Manifest.permission.ACCESS_FINE_LOCATION) != PackageManager.PERMISSION_GRANTED && ActivityCompat.checkSelfPermission(this, android.Manifest.permission.ACCESS_COARSE_LOCATION) != PackageManager.PERMISSION_GRANTED) {
            // TODO: Consider calling
            //    ActivityCompat#requestPermissions
            // here to request the missing permissions, and then overriding
            //   public void onRequestPermissionsResult(int requestCode, String[] permissions,
            //                                          int[] grantResults)
            // to handle the case where the user grants the permission. See the documentation
            // for ActivityCompat#requestPermissions for more details.
            return Service.START_NOT_STICKY;
        }
        try {
            // locationManager.requestLocationUpdates(LocationManager.GPS_PROVIDER, TWO_MINUTES, 0, listener);
            locationManager.requestLocationUpdates(LocationManager.NETWORK_PROVIDER, TWO_MINUTES, 0, listener);
            // Toast.makeText( getApplicationContext(), "GPS Send!!", Toast.LENGTH_SHORT ).show();
        }
        catch (Exception e){
            Log.d("MyApp", String.valueOf(e));
            locationManager.requestLocationUpdates(LocationManager.NETWORK_PROVIDER, TWO_MINUTES, 0, listener);
        }
        return START_STICKY; // or other appropriate return value
    }

   

    @Override
    public IBinder onBind(Intent intent) {
        return null;
    }


    public void stop_locservice() {
        locationManager.removeUpdates(listener);
        Log.v("LocationService", "Service stopped");
    }

    private class MyLocationListener implements LocationListener {

        @Override
        public void onLocationChanged(Location loc) {
            Log.i("LocationListener", "Location changed");
            // Toast.makeText( getApplicationContext(),"Loc Recive", Toast.LENGTH_SHORT ).show();
            sendLocationBroadcast(loc);

            String l = "LON:" + String.valueOf(loc.getLongitude()) + " LAT:" + String.valueOf(loc.getLatitude());

            Log.d("LOCATION", l);
            // Toast.makeText( getApplicationContext(), l, Toast.LENGTH_SHORT ).show();

        }

        @Override
        public void onProviderDisabled(String provider) {
            Toast.makeText(getApplicationContext(), "GPS Disabled", Toast.LENGTH_SHORT).show();
        }

        @Override
        public void onProviderEnabled(String provider) {
            Toast.makeText(getApplicationContext(), "GPS Enabled", Toast.LENGTH_SHORT).show();
        }

        @Override
        public void onStatusChanged(String provider, int status, Bundle extras) {
            // Handle status changes if needed
        }
    }



    private void sendLocationBroadcast(Location location) {
        Intent broadcastIntent = new Intent(BROADCAST_ACTION);
        broadcastIntent.setClass(this,LocationReceiver.class);
        broadcastIntent.putExtra("Latitude", String.valueOf(location.getLatitude()));
        broadcastIntent.putExtra("Longitude", String.valueOf(location.getLongitude()));
        broadcastIntent.putExtra("Provider", location.getProvider());
        sendBroadcast(broadcastIntent);
        stop_locservice();
        // Toast.makeText(getApplicationContext(), "Not Null", Toast.LENGTH_SHORT).show();

    }   
}
