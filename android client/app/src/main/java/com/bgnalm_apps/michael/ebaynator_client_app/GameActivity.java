package com.bgnalm_apps.michael.ebaynator_client_app;

import android.app.Activity;
import android.content.Intent;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.view.animation.AnimationUtils;
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

public class GameActivity extends Activity {

    final String NEXT_QUESTION_URL = "http://bgnalm.pythonanywhere.com/next_question";

    String key;
    String question;
    String result;
    int questionId = 0;
    TextView questionText;
    boolean wasLastResponseAnswer = false;


    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_game);
        this.questionText = (TextView) findViewById(R.id.question_text);
        Bundle bundle = getIntent().getExtras();
        this.key = bundle.getString("key");
        this.question = bundle.getString("question");
        this.questionId = bundle.getInt("questionId");
        this.updateQuestionText();
    }

    public void startResultActivity(){
        Log.d("bgnalm", "starting result activity with result: "+this.result);
        Intent intent = new Intent(this, ResultActivity.class);
        intent.putExtra("key", this.key);
        intent.putExtra("result", this.result);
        startActivity(intent);
        finish();
    }
    public void updateQuestionText(){
        this.questionText.setText(this.question);
        this.questionText.startAnimation(AnimationUtils.loadAnimation(GameActivity.this, android.R.anim.fade_in));
    }

    public String generateNextQuestionRequest(String answer){
        JSONObject request = new JSONObject();
        try {
            request.put("key", this.key);
            request.put("answer", answer);
            request.put("question_id", this.questionId);
        } catch (JSONException e) {
            Log.d("bgnalm", "error with json creation");
            e.printStackTrace();
        }

        return request.toString();
    }

    public void loadResponse(String jsonResponse){
        JSONObject response;
        try {
            response = new JSONObject(jsonResponse);
            if (response.has("error") || response.has("result")) {
                this.wasLastResponseAnswer = true;
                if (response.has("error")) {
                    this.result = response.getString("error");
                }
                else {
                    this.result = response.getString("result");
                }
            }
            else {
                this.key = response.getString("key");
                this.questionId = response.getInt("question_id");
                this.question = response.getString("question");
            }
        } catch (JSONException e) {
            Log.d("bgnalm", "error with response to json");
            e.printStackTrace();
        }
    }

    public void sendAnswer(String answer) {
        try {
            HttpClient httpclient = new DefaultHttpClient();
            HttpPost post = new HttpPost(NEXT_QUESTION_URL);
            String nextQuestionJsonRequest = this.generateNextQuestionRequest(answer);
            StringEntity se=new StringEntity(nextQuestionJsonRequest);
            post.setEntity(se);
            HttpResponse response = httpclient.execute(post);
            StatusLine statusLine = response.getStatusLine();
            if (statusLine.getStatusCode() == HttpStatus.SC_OK) {
                ByteArrayOutputStream out = new ByteArrayOutputStream();
                response.getEntity().writeTo(out);
                String jsonStringResponse = out.toString();
                Log.d("bgnalm", "response: "+jsonStringResponse);
                this.loadResponse(jsonStringResponse);
                out.close();
            } else {
                response.getEntity().getContent().close();
                throw new IOException(statusLine.getReasonPhrase());
            }
        } catch (Exception e){
            e.printStackTrace();
        }
    }

    public void buttonClick(View view){
        String answer="";
        switch (view.getId()) {
            case (R.id.yes_button):
                answer = "yes";
                break;
            case (R.id.no_button):
                answer = "no";
                break;
            case (R.id.prob_button):
                answer = "probably";
                break;
            case (R.id.prob_not_button):
                answer = "probably not";
                break;
            case (R.id.dont_know_button):
                answer = "dont know";
                break;
        }

        this.sendAnswer(answer);

        if (this.wasLastResponseAnswer){
            this.startResultActivity();
        }
        else {
            this.updateQuestionText();
        }
    }



}
