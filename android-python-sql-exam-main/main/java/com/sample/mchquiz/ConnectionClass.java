package com.sample.mchquiz;

import android.annotation.SuppressLint;
import android.content.SharedPreferences;
import android.os.StrictMode;
import android.preference.PreferenceManager;
import android.support.v7.app.AppCompatActivity;
import android.util.Log;
import android.widget.EditText;
import android.widget.Toast;

import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.SQLException;

import android.content.Intent;
/**
 * Created by ABHI on 9/20/2016.
 */
public class ConnectionClass extends AppCompatActivity {

    String classs = "com.mysql.jdbc.Driver";
    //String ipaddress = getIntent().getStringExtra("IPADDRESS");
    //String ipaddress = "192.168.0.107";
    //String ipaddress;

    //String url = "jdbc:mysql://"+ipaddress+"/ece109";
    String url;
    String un = "francis";
    String password = "1234";



    //String ipaddress = pref.getString("key_name", null);

    @SuppressLint("NewApi")
    public Connection CONN(String ipaddress,String subject) {
        //editTextAddress = (EditText) findViewById(R.id.serverip);
        //ipaddress = editTextAddress.getText().toString();;

        StrictMode.ThreadPolicy policy = new StrictMode.ThreadPolicy.Builder()
                .permitAll().build();
        StrictMode.setThreadPolicy(policy);
        Connection conn = null;
        String ConnURL = null;
        try {

            Class.forName(classs);

            url = "jdbc:mysql://"+ipaddress+"/"+subject;

            conn = DriverManager.getConnection(url, un, password);


            conn = DriverManager.getConnection(ConnURL);
        } catch (SQLException se) {
            Log.e("ERRO", se.getMessage());
        } catch (ClassNotFoundException e) {
            Log.e("ERRO", e.getMessage());
        } catch (Exception e) {
            Log.e("ERRO", e.getMessage());
        }
        return conn;

    }

}