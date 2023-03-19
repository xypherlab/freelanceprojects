package com.sample.mchquiz;

import android.content.Context;
import android.content.Intent;
import android.net.wifi.WifiManager;
import android.os.Bundle;
import android.provider.Settings;
import android.support.v7.app.AppCompatActivity;
import android.view.View;
import android.widget.EditText;
import android.widget.TextView;
import android.widget.Toast;

import java.sql.Connection;
import java.sql.ResultSet;
import java.sql.Statement;

public class IPActivity extends AppCompatActivity {
    String ipaddress;
    String subject;
    String quizsel;
    String username;
    String userpassword;
    String ipadd;
    EditText editTextAddress;
    EditText subjectchoice;
    EditText quizchoice;
    EditText userinput;
    EditText passwordinput;

    ConnectionClass2 connectionClass2;
    ConnectionClass3 connectionClass3;


    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.hostipconnection);
        String androidID = Settings.Secure.getString(getContentResolver(), Settings.Secure.ANDROID_ID);
        //WifiManager wifi = (WifiManager)getApplicationContext().getSystemService(Context.WIFI_SERVICE);
        //String wanMAC = wifi .getConnectionInfo().getMacAddress();
        TextView uniqueid = (TextView)findViewById(R.id.deviceid);
        //TextView macid = (TextView)findViewById(R.id.macid);
        uniqueid.setText("Device ID: "+androidID);
        //macid.setText("MAC Address: "+wanMAC);

    }

    public void onStartClick(View view) {

        Intent intent = new Intent(IPActivity.this, QuizActivity.class);
        editTextAddress = (EditText) findViewById(R.id.serverip);
        subjectchoice = (EditText) findViewById(R.id.subject);
        quizchoice = (EditText) findViewById(R.id.quiz);
        userinput = (EditText) findViewById(R.id.loginuser);
        passwordinput= (EditText) findViewById(R.id.loginpassword);

        ipaddress = editTextAddress.getText().toString();
        ipadd = editTextAddress.getText().toString();
        subject =subjectchoice.getText().toString();
        quizsel=quizchoice.getText().toString();
        //Toast.makeText(IPActivity.this, ipaddress, Toast.LENGTH_SHORT).show();
        username = userinput.getText().toString();
        userpassword =passwordinput.getText().toString();
        connectionClass2 = new ConnectionClass2();
        connectionClass3 = new ConnectionClass3();
        int a=0;
        int b=0;
        int c=0;
        int d=0;
        int e=0;
        try {
            Connection con = connectionClass2.CONN(ipadd);

            String query="select * from `credentials` where username='"+username+"'";
            Statement stmt = con.createStatement();
            ResultSet rs=stmt.executeQuery(query);
           while (rs.next()) {
                String usercmp= String.valueOf(rs.getString(1));

                String passwordcmp= String.valueOf(rs.getString(2));
                String androidID = Settings.Secure.getString(getContentResolver(), Settings.Secure.ANDROID_ID);
                //WifiManager wifi = (WifiManager)getApplicationContext().getSystemService(Context.WIFI_SERVICE);
                //String wanMAC = wifi .getConnectionInfo().getMacAddress();
                String deviceidcmp= String.valueOf(rs.getString(3));
                //String macaddresscmp= String.valueOf(rs.getString(4));

                if(usercmp.equals(username))
                {
                a=1;

                }
                else
                {
                    Toast.makeText(IPActivity.this, "Username not registered!", Toast.LENGTH_SHORT).show();
                }
                if(passwordcmp.equals(userpassword))
                {
                    b=1;

                }
                else
                {
                    Toast.makeText(IPActivity.this, "Wrong password!", Toast.LENGTH_SHORT).show();
                }
                if(deviceidcmp.equals(androidID))
                {
                    c=1;

                }
                else
                {
                    Toast.makeText(IPActivity.this, "Device ID not matched with user's info!", Toast.LENGTH_SHORT).show();
                }

            }


        }
        catch (Exception ex)
        {
            Toast.makeText(IPActivity.this, "Username not found!", Toast.LENGTH_SHORT).show();
        }
        if(a==1 && b==1 && c==1 ) {
            try {
                e=1;
                Connection cona = connectionClass3.CONN(ipadd, subject);

                String query = "select * from `"+quizsel+"` where studentname='" + username + "'";
                Statement stmta = cona.createStatement();
                ResultSet rsa = stmta.executeQuery(query);
                while (rsa.next()) {
                    String usercmpo= String.valueOf(rsa.getString(1));
                    if(usercmpo.equals(username))
                    {
                        e=0;

                    }

                }
            }
            catch (Exception ex)
            {
                Toast.makeText(IPActivity.this, "Something went wrong!", Toast.LENGTH_SHORT).show();
            }

        }

        if (e==1)
        {  try {Connection cona = connectionClass3.CONN(ipadd, subject);
            String androidID = Settings.Secure.getString(getContentResolver(), Settings.Secure.ANDROID_ID);
            //WifiManager wifi = (WifiManager)getApplicationContext().getSystemService(Context.WIFI_SERVICE);
            //String wanMAC = wifi .getConnectionInfo().getMacAddress();

            String query = "insert into `"+quizsel+"` values ('"+username+"','"+androidID+"')";
            Statement stmta = cona.createStatement();
            stmta.executeUpdate(query);
        }
        catch (Exception ex)
        {
            Toast.makeText(IPActivity.this, "Something went wrong!", Toast.LENGTH_SHORT).show();
        }
            intent.putExtra("ipselect", ipaddress);
            intent.putExtra("subjectselect", subject);
            intent.putExtra("quizselect", quizsel);
            startActivity(intent);
        }
        else
        {
            Toast.makeText(IPActivity.this, "Exam not available!", Toast.LENGTH_SHORT).show();
        }
        /*editTextAddress.getText().clear();
        subjectchoice.getText().clear();
        quizchoice.getText().clear();
        userinput.getText().clear();
        passwordinput.getText().clear();*/

    }

}

