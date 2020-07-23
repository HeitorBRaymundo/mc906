package com.example.harrypotterspells;

import androidx.annotation.RequiresApi;
import androidx.appcompat.app.AppCompatActivity;

import android.content.Context;
import android.hardware.Sensor;
import android.hardware.SensorEvent;
import android.hardware.SensorEventListener;
import android.hardware.SensorManager;
import android.os.Build;
import android.os.Bundle;
import android.view.MotionEvent;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.Toast;

import com.android.volley.Request;
import com.android.volley.RequestQueue;
import com.android.volley.Response;
import com.android.volley.VolleyError;
import com.android.volley.toolbox.JsonObjectRequest;
import com.android.volley.toolbox.Volley;

import org.json.JSONException;
import org.json.JSONObject;

public class MainActivity extends AppCompatActivity implements SensorEventListener {

    private SensorManager sensorManager;
    private Sensor accelerometerSensor;
    private Sensor gravitySensor;
    private Sensor gyroscopeSensor;
    private Sensor linearAccelerationSensor;
    private Sensor rotationVectorSensor;
    private Sensor magneticFieldSensor;

    private StringBuilder sensorData;

    private final float[] accelerometerReading = new float[3];
    private final float[] magnetometerReading = new float[3];

    private final float[] rotationMatrix = new float[9];
    private final float[] orientationAngles = new float[3];

    private boolean updatedAcc;
    private boolean updatedMag;

    private Button btnSpell;
    private EditText txtIp, txtPort;

    private boolean recording;
    private RequestQueue requestQueue;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        sensorManager = (SensorManager) getSystemService(Context.SENSOR_SERVICE);

        accelerometerSensor         = sensorManager.getDefaultSensor(Sensor.TYPE_ACCELEROMETER);
        gravitySensor               = sensorManager.getDefaultSensor(Sensor.TYPE_GRAVITY);
        gyroscopeSensor             = sensorManager.getDefaultSensor(Sensor.TYPE_GYROSCOPE);
        linearAccelerationSensor    = sensorManager.getDefaultSensor(Sensor.TYPE_LINEAR_ACCELERATION);
        rotationVectorSensor        = sensorManager.getDefaultSensor(Sensor.TYPE_ROTATION_VECTOR);
        magneticFieldSensor         = sensorManager.getDefaultSensor(Sensor.TYPE_MAGNETIC_FIELD);


        btnSpell = findViewById(R.id.btnSpell);
        txtIp = findViewById(R.id.txtIp);
        txtPort = findViewById(R.id.txtPort);


        requestQueue = Volley.newRequestQueue(this);

        btnSpell.setOnTouchListener(new View.OnTouchListener() {
            @Override
            public boolean onTouch(View view, MotionEvent motionEvent) {
                if (btnSpell.isEnabled()) {

                    if (motionEvent.getAction() == MotionEvent.ACTION_DOWN) {
                        startRecord();
                    } else if (motionEvent.getAction() == MotionEvent.ACTION_UP) {
                        sendRecord();
                    }
                }
                return false;
            }
        });

        recording = false;
        sensorData = new StringBuilder();
    }

    private void zeroVector(float[] vector){
        for(int i=0; i<vector.length; i++)
            vector[i] = 0;
    }

    private void startRecord(){
        zeroVector(rotationMatrix);
        zeroVector(orientationAngles);
        updatedAcc = false;
        updatedMag = false;
        sensorData = new StringBuilder();
        recording = true;
    }



    private void sendRecord(){
        recording = false;
        btnSpell.setEnabled(false);

        try {
            String URL = "http://"+txtIp.getText().toString()+":"+txtPort.getText().toString()+"/collect";
            JSONObject jsonBody = new JSONObject();
            jsonBody.put("data", sensorData.toString());

            JsonObjectRequest request = new JsonObjectRequest(Request.Method.POST, URL,
                    jsonBody, new Response.Listener<JSONObject>() {
                @Override
                public void onResponse(JSONObject response) {
                    btnSpell.setEnabled(true);
                }
            }, new Response.ErrorListener() {
                @Override
                public void onErrorResponse(VolleyError error) {
                    toast("Erro: "+error.getMessage());
                    btnSpell.setEnabled(true);
                }
            });

            requestQueue.add(request);

        } catch (JSONException e) {
            toast(e.getMessage());
        }
    }

    private String toStringArrayFloat(float[] data, int size){

        StringBuilder result = new StringBuilder();

        for (int i=0; i<size-1; i++)
            result.append(data[i]).append(", ");
        result.append(data[size-1]);

        return result.toString();
    }

    @Override
    public void onSensorChanged(SensorEvent sensorEvent) {
        //Log.d("MainActivity", sensorEvent.sensor.getName()+": "+sensorEvent.timestamp+", "+ Arrays.toString(sensorEvent.values));

        String sensorStringData = null;
        double timestamp = sensorEvent.timestamp/1000000.0;

        if (sensorEvent.sensor.getType() == Sensor.TYPE_ACCELEROMETER) {
            System.arraycopy(sensorEvent.values, 0, accelerometerReading,0, accelerometerReading.length);
            sensorStringData = "ACC, "+timestamp+", "+toStringArrayFloat(sensorEvent.values, 3)+"\n";
            updatedAcc = true;
        } else if (sensorEvent.sensor.getType() == Sensor.TYPE_MAGNETIC_FIELD) {
            System.arraycopy(sensorEvent.values, 0, magnetometerReading,0, magnetometerReading.length);
            sensorStringData = "MAG, "+timestamp+", "+toStringArrayFloat(sensorEvent.values, 3)+"\n";
            updatedMag = true;
        } else if (sensorEvent.sensor.getType() == Sensor.TYPE_GRAVITY) {
            sensorStringData = "GRA, "+timestamp+", "+toStringArrayFloat(sensorEvent.values, 3)+"\n";
        } else if (sensorEvent.sensor.getType() == Sensor.TYPE_GYROSCOPE) {
            sensorStringData = "GYR, "+timestamp+", "+toStringArrayFloat(sensorEvent.values, 3)+"\n";
        } else if (sensorEvent.sensor.getType() == Sensor.TYPE_LINEAR_ACCELERATION) {
            sensorStringData = "LAC, "+timestamp+", "+toStringArrayFloat(sensorEvent.values, 3)+"\n";
        } else if (sensorEvent.sensor.getType() == Sensor.TYPE_ROTATION_VECTOR) {
            sensorStringData = "RTV, "+timestamp+", "+toStringArrayFloat(sensorEvent.values, 4)+"\n";
        }
        if ((recording) && (sensorStringData!=null)) {
            sensorData.append(sensorStringData);

            if (updatedMag && updatedAcc) {
                updateOrientationAngles(timestamp);
                updatedAcc = false;
                updatedMag = false;
            }
        }
    }

    public void updateOrientationAngles(double timestamp) {
        SensorManager.getRotationMatrix(rotationMatrix, null,
                accelerometerReading, magnetometerReading);

        sensorData.append("RTM, "+timestamp+", "+toStringArrayFloat(rotationMatrix, 9)+"\n");
        SensorManager.getOrientation(rotationMatrix, orientationAngles);
        sensorData.append("ORI, "+timestamp+", "+toStringArrayFloat(orientationAngles, 3)+"\n");
    }

    private void toast(String message){
        Toast.makeText(this, message, Toast.LENGTH_SHORT).show();
    }

    @Override
    public void onAccuracyChanged(Sensor sensor, int i) {

    }

    private boolean registerSensor(Sensor sensor){
        if (sensor!=null){
            sensorManager.registerListener(this, sensor, SensorManager.SENSOR_DELAY_FASTEST);
            return true;
        }
        return false;
    }

    @Override
    protected void onResume() {

        super.onResume();
        if (!registerSensor(accelerometerSensor))
            toast("Não contém accelerometerSensor");

        if (!registerSensor(gravitySensor))
            toast("Não contém sensor gravitySensor");

        if (!registerSensor(gyroscopeSensor))
            toast("Não contém sensor gyroscopeSensor");

        if (!registerSensor(linearAccelerationSensor))
            toast("Não contém sensor linearAccelerationSensor");

        if (!registerSensor(rotationVectorSensor))
            toast("Não contém sensor rotationVectorSensor");

        if (!registerSensor(magneticFieldSensor))
            toast("Não contém sensor magneticFieldSensor");

    }

    @Override
    protected void onPause() {
        super.onPause();
        sensorManager.unregisterListener(this);
    }

    @Override
    protected void onDestroy(){
        super.onDestroy();
    }

}