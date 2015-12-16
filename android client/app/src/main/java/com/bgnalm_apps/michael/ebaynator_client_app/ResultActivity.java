package com.bgnalm_apps.michael.ebaynator_client_app;

import android.app.Activity;
import android.os.StrictMode;
import android.os.Bundle;
import android.util.Log;
import android.view.KeyEvent;
import android.view.View;
import android.view.animation.Animation;
import android.view.animation.AnimationUtils;
import android.widget.EditText;
import android.widget.TextView;

import org.apache.http.HttpResponse;
import org.apache.http.HttpStatus;
import org.apache.http.StatusLine;
import org.apache.http.client.HttpClient;
import org.apache.http.client.methods.HttpPost;
import org.apache.http.entity.StringEntity;
import org.apache.http.impl.client.DefaultHttpClient;
import org.json.JSONException;
import org.json.JSONObject;

import java.io.ByteArrayOutputStream;
import java.io.IOException;

public class ResultActivity extends Activity {

    final int END_WAIT_TIME = 1000;
    final String RESULT_URL = "http://bgnalm.pythonanywhere.com/result";

    boolean answered;

    String key;
    String result;

    TextView resultText;
    TextView endText;
    EditText insertText;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_result);
        StrictMode.ThreadPolicy policy = new StrictMode.ThreadPolicy.Builder().permitAll().build();
        StrictMode.setThreadPolicy(policy);

        Bundle bundle = getIntent().getExtras();
        this.key = bundle.getString("key");
        this.result = bundle.getString("result");
        this.answered = false;

        this.resultText = (TextView) findViewById(R.id.resultText);
        this.endText = (TextView) findViewById(R.id.endText);
        this.insertText = (EditText) findViewById(R.id.insertText);

        this.resultText.setText(this.result);
        Animation resultTextAnimation = AnimationUtils.loadAnimation(getApplicationContext(), R.anim.abc_fade_in);
        this.resultText.startAnimation(resultTextAnimation);

        this.insertText.setOnKeyListener(new View.OnKeyListener() {

            @Override
            public boolean onKey(View v, int keyCode, KeyEvent event) {
                if (event.KEYCODE_ENTER == keyCode && event.getAction() == event.ACTION_DOWN) {
                    sendResult(insertText.getText().toString());
                    insertText.setVisibility(View.INVISIBLE);
                    animateEndText();
                    return true;
                }

                return false;
            }
        });
    }


    public String generateJsonResult(String resultToSend){
        String toReturn="";
        JSONObject jsonObject = new JSONObject();
        try {
            jsonObject.put("key", this.key);
            jsonObject.put("result", resultToSend);
            toReturn = jsonObject.toString();
        } catch (JSONException e) {
            e.printStackTrace();
        }

        return toReturn;
    }

    public void sendResult(String result){
        Log.d("bgnalm", "sending result: "+result);
        if (this.answered == true) {
            return;
        }

        this.answered = true;

        try {
            HttpClient httpclient = new DefaultHttpClient();
            HttpPost post = new HttpPost(RESULT_URL);
            String nextQuestionJsonRequest = this.generateJsonResult(result);
            StringEntity se=new StringEntity(nextQuestionJsonRequest);
            post.setEntity(se);
            HttpResponse response = httpclient.execute(post);
            StatusLine statusLine = response.getStatusLine();
            if (statusLine.getStatusCode() == HttpStatus.SC_OK) {
                ByteArrayOutputStream out = new ByteArrayOutputStream();
                response.getEntity().writeTo(out);
                String jsonStringResponse = out.toString();
                Log.d("bgnalm", " result response: " + jsonStringResponse);
                out.close();
            } else {
                response.getEntity().getContent().close();
                throw new IOException(statusLine.getReasonPhrase());
            }
        } catch (Exception e){
            e.printStackTrace();
        }
    }

    public void animateEndText() {
        this.endText.setEnabled(true);
        this.endText.setVisibility(View.VISIBLE);
        Animation animation = AnimationUtils.loadAnimation(getApplicationContext() , R.anim.abc_slide_in_bottom);
        animation.setAnimationListener(new Animation.AnimationListener() {

            @Override
            public void onAnimationStart(Animation animation) {

            }

            @Override
            public void onAnimationRepeat(Animation animation) {
            }

            @Override
            public void onAnimationEnd(Animation animation) {
                finishGame();
            }

        });
        this.endText.startAnimation(animation);
    }

    public void waitMillis(int millis){
        Long startTime = System.currentTimeMillis();
        while(System.currentTimeMillis()-startTime < millis) {}
    }

    public void finishGame(){
        this.waitMillis(END_WAIT_TIME);
        finish();
    }

    public void guessIsRight(View v){
        Log.d("bgnalm", "guess was right");
        this.sendResult(this.result);
        this.animateEndText();
    }

    public void guessIsWrong(View v) {
        Log.d("bgnalm", "guesss was wrong");
        this.insertText.setVisibility(View.VISIBLE);
        this.insertText.setEnabled(true);
    }



}
