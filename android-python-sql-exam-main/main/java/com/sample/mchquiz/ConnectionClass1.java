package com.sample.mchquiz;

import android.annotation.SuppressLint;
import android.os.StrictMode;
import android.support.v7.app.AppCompatActivity;
import android.util.Log;
import android.widget.EditText;
import android.widget.Toast;

import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.SQLException;

/**
 * Created by ABHI on 9/20/2016.
 */
public class ConnectionClass1 extends AppCompatActivity {
    EditText editTextAddress;
    String classs = "com.mysql.jdbc.Driver";
    //String ipaddress = getIntent().getStringExtra("IPADDRESS");
    //String ipaddress="192.168.0.107";

    //String url = "jdbc:mysql://"+ipaddress+"/ece109";
    String url;
    //String url = "jdbc:mysql://"+ipaddress+"/ece109results";
    String un = "francis";
    String password = "1234";



    @SuppressLint("NewApi")
    public Connection CONN(String ipaddress,String subject) {
        StrictMode.ThreadPolicy policy = new StrictMode.ThreadPolicy.Builder()
                .permitAll().build();
        StrictMode.setThreadPolicy(policy);
        Connection conn = null;
        String ConnURL = null;
        try {

            Class.forName(classs);
            //editTextAddress = (EditText) findViewById(R.id.serverip);
            //ipaddress = editTextAddress.getText().toString();;
            url = "jdbc:mysql://"+ipaddress+"/"+subject+"results";
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