package com.example.cagetcpcom;

import android.content.Context;
import android.content.SharedPreferences;
import android.os.CountDownTimer;
import android.preference.PreferenceManager;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.text.Editable;
import android.text.TextWatcher;
import android.text.method.ScrollingMovementMethod;
import android.view.View;
import android.view.View.OnClickListener;
import android.webkit.WebChromeClient;
import android.webkit.WebSettings;
import android.webkit.WebView;
import android.widget.Button;
import android.widget.EditText;
import android.widget.TextView;
import android.widget.Toast;
import android.widget.ToggleButton;

public class MainActivity extends AppCompatActivity {

    TextView response;
    EditText editTextAddress;
    Button buttonConnect, buttonClear;
    String editTextPort;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        final ToggleButton tb1 = (ToggleButton)findViewById(R.id.toggleButton);
        editTextAddress = (EditText) findViewById(R.id.addressEditText);
        editTextPort = "80";
        buttonConnect = (Button) findViewById(R.id.connectButton);
        buttonClear = (Button) findViewById(R.id.clearButton);
        response = (TextView) findViewById(R.id.responseTextView);
        final SharedPreferences prefs = PreferenceManager
                .getDefaultSharedPreferences(this);

        editTextAddress.setText(prefs.getString("autoSave", ""));


        editTextAddress.addTextChangedListener(new TextWatcher() {
            @Override
            public void onTextChanged(CharSequence s, int start, int before,
                                      int count)
            {
            }

            @Override
            public void beforeTextChanged(CharSequence s, int start, int count,
                                          int after)
            {
            }

            @Override
            public void afterTextChanged(Editable s)
            {
                prefs.edit().putString("autoSave", s.toString()).commit();
            }
        });
        buttonConnect.setOnClickListener(new View.OnClickListener() {
            public void onClick(View v) {
                String ipstr = editTextAddress.getText().toString();
                String ipaddress="http://"+ipstr+":5000/video_feed";
                Toast msg = Toast.makeText(getBaseContext(),ipaddress,Toast.LENGTH_LONG);
                msg.show();
                WebView webView = (WebView) findViewById(R.id.webView);
                webView.setWebChromeClient(new WebChromeClient());
                webView.getSettings().setPluginState(WebSettings.PluginState.ON_DEMAND);
                webView.getSettings().setJavaScriptEnabled(true);
                webView.getSettings().setBuiltInZoomControls(true);

                webView.getSettings().setUseWideViewPort(true);
                webView.getSettings().setLoadWithOverviewMode(true);
                webView.setInitialScale(1);
                //webView.loadUrl("http://192.168.43.214:5000/video_feed");
                webView.loadUrl(ipaddress);

            }
        });
        tb1.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                boolean status;
                if (tb1.isChecked()) {
                    status = true;
                    new CountDownTimer(1000, 1000)
                    {

                        public void onTick(long millisUntilFinished)
                        {

                        }

                        public void onFinish()
                        {
                            response.setMovementMethod(new ScrollingMovementMethod());
                            Client myClient = new Client(editTextAddress.getText()
                                    .toString(), Integer.parseInt(editTextPort
                                    .toString()), response);
                            myClient.execute();


                            start();
                        }
                    }.start();
                } else {
                    status = false;

                }
            }
        });


        buttonClear.setOnClickListener(new OnClickListener() {

            @Override
            public void onClick(View v) {
                response.setText("");
            }
        });
    }


}
