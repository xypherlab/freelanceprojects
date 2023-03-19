package com.sample.mchquiz;

import android.annotation.SuppressLint;
import android.os.StrictMode;
import android.support.v7.app.AppCompatActivity;
import android.util.Log;
import android.widget.EditText;

import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.SQLException;

/**
 * Created by ABHI on 9/20/2016.
 */
public class ConnectionClass3 extends AppCompatActivity {
    EditText editTextAddress;
    String classs = "com.mysql.jdbc.Driver";
    String url;
    String un = "francis";
    String password = "1234";
    //String ipaddress="192.168.0.100";


    @SuppressLint("NewApi")
    public Connection CONN(String ipadd, String quizs) {
        StrictMode.ThreadPolicy policy = new StrictMode.ThreadPolicy.Builder()
                .permitAll().build();
        StrictMode.setThreadPolicy(policy);
        Connection conn = null;
        String ConnURL = null;
        try {

            Class.forName(classs);

            url = "jdbc:mysql://"+ipadd+"/"+quizs+"attendance";
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