package com.bgnalm_apps.michael.ebaynator_client_app;

import android.app.Activity;
import android.content.Intent;
import android.os.StrictMode;
import android.os.Bundle;
import android.util.Log;
import android.view.View;

import org.apache.http.HttpResponse;
import org.apache.http.HttpStatus;
import org.apache.http.StatusLine;
import org.apache.http.client.HttpClient;
import org.apache.http.client.methods.HttpGet;
import org.apache.http.impl.client.DefaultHttpClient;
import org.json.JSONException;
import org.json.JSONObject;

import java.io.ByteArrayOutputStream;
import java.io.IOException;


public class MenuActivity extends Activity {

    final String START_URL = "http://bgnalm.pythonanywhere.com/start";
    String key = "";
    String firstQuestion = "";
    int questionId = 0;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_menu);
        StrictMode.ThreadPolicy policy = new StrictMode.ThreadPolicy.Builder().permitAll().build();
        StrictMode.setThreadPolicy(policy);
    }

    public void switchToGameActivity(){
        Intent intent = new Intent(this, GameActivity.class);
        intent.putExtra("key", this.key);
        intent.putExtra("question", this.firstQuestion);
        intent.putExtra("questionId", this.questionId);
        Log.d("bgnalm", "starting with key:" + this.key + " question: " + this.firstQuestion);
        startActivity(intent);
    }

    private void parseJson(String jsonString) {
        try {
            JSONObject jsonObj = new JSONObject(jsonString);
            this.key = jsonObj.getString("key");
            this.firstQuestion = jsonObj.getString("question");
            this.questionId = jsonObj.getInt("question_id");
        } catch (JSONException e) {
            Log.d("bgnalm", "error with json parseing");
            e.printStackTrace();
        }
    }

    public boolean getKeyAndQuestion(){
        try {
            HttpClient httpclient = new DefaultHttpClient();
            HttpResponse response = httpclient.execute(new HttpGet(START_URL));
            StatusLine statusLine = response.getStatusLine();
            if (statusLine.getStatusCode() == HttpStatus.SC_OK) {
                ByteArrayOutputStream out = new ByteArrayOutputStream();
                response.getEntity().writeTo(out);
                this.parseJson(out.toString());
                out.close();
                return true;
            } else {
                response.getEntity().getContent().close();
                throw new IOException(statusLine.getReasonPhrase());
            }
        } catch (Exception e){
            e.printStackTrace();
            return false;
        }
    }

    public void startGame(View v){
        Log.d("bgnalm", "starting game");
        if (getKeyAndQuestion()){
            this.switchToGameActivity();
        }
        else {
            Log.d("bgnalm", "failed to get key and question");
        }


    }



}
