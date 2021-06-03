package com.project.iotdataviewer;

import androidx.appcompat.app.AppCompatActivity;

import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.ProgressBar;
import android.widget.TextView;
import android.widget.Toast;

import com.android.volley.Request;
import com.android.volley.RequestQueue;
import com.android.volley.Response;
import com.android.volley.VolleyError;
import com.android.volley.toolbox.StringRequest;
import com.android.volley.toolbox.Volley;

public class MainActivity extends AppCompatActivity {

    private TextView txtTmp;
    private TextView txtHmd;
    private TextView txtCmx;
    private ProgressBar progressBar;
    private Button btnRefresh;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        txtTmp = findViewById(R.id.txtTmp);
        txtHmd = findViewById(R.id.txtHmd);
        txtCmx = findViewById(R.id.txtCmx);
        progressBar = findViewById(R.id.progressBar);
        progressBar.setVisibility(View.GONE);
        btnRefresh = findViewById(R.id.btnRefresh);

        RefreshDatas();

        btnRefresh.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                RefreshDatas();
            }
        });

    }

    private void RefreshDatas(){

        progressBar.setVisibility(View.VISIBLE);
        btnRefresh.setClickable(false);

        String url = "localhost/refresh";

        RequestQueue requestQueue = Volley.newRequestQueue(this);

        StringRequest stringRequest = new StringRequest(Request.Method.GET, url,
                new Response.Listener<String>() {
                    @Override
                    public void onResponse(String response) {
                        String data = response;
                        txtTmp.setText(data.split(",")[0]+"C");
                        txtHmd.setText(data.split(",")[1]+"%");
                        txtCmx.setText(data.split(",")[2]+"%");
                        Toast.makeText(getApplicationContext(), "Datas Refreshed", Toast.LENGTH_SHORT).show();
                        progressBar.setVisibility(View.GONE);
                        btnRefresh.setClickable(true);
                    }
                },
                new Response.ErrorListener() {
                    @Override
                    public void onErrorResponse(VolleyError error) {
                        Toast.makeText(getApplicationContext(), "An Error Occured !", Toast.LENGTH_SHORT).show();
                        btnRefresh.setClickable(true);
                    }
                });

        requestQueue.add(stringRequest);
    }

}
