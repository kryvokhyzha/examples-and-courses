package com.example.lab4;

import androidx.annotation.RequiresApi;
import androidx.appcompat.app.AppCompatActivity;

import android.media.AudioAttributes;
import android.media.MediaPlayer;
import android.net.Uri;
import android.os.Build;
import android.os.Bundle;
import android.view.View;
import android.widget.ArrayAdapter;
import android.widget.EditText;
import android.widget.MediaController;
import android.widget.RadioButton;
import android.widget.Spinner;
import android.widget.Toast;
import android.widget.VideoView;

import java.io.IOException;

public class MainActivity extends AppCompatActivity {
    private VideoView videoPlayer;
    private MediaPlayer mediaPlayer;

    private Spinner itemSpinner;

    private boolean videoIsSelect = true;

    @RequiresApi(api = Build.VERSION_CODES.LOLLIPOP)
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        final String[] items = getResources().getStringArray(R.array.items);

        itemSpinner = findViewById(R.id.items);

        ArrayAdapter<String> groupAdapter = new ArrayAdapter(this,
                android.R.layout.simple_spinner_item, items);
        groupAdapter.setDropDownViewResource(android.R.layout.simple_spinner_dropdown_item);

        itemSpinner.setAdapter(groupAdapter);

        videoPlayer = findViewById(R.id.videoPlayer);
        // videoPlayer.setVideoURI(myVideoUri);
       // videoPlayer.setVideoPath("http://video.ch9.ms/ch9/507d/71f4ef0f-3b81-4d2c-956f-c56c81f9507d/AndroidEmulatorWithMacEmulator.mp4");

        MediaController mediaController = new MediaController(this);
        videoPlayer.setMediaController(mediaController);
        mediaController.setMediaPlayer(videoPlayer);

        mediaPlayer = new MediaPlayer();
    }

    public void play(View view) {
        String item = itemSpinner.getSelectedItem().toString();

        if (videoIsSelect) {
            if (item.equals("URL")) {
                EditText edtEditText = findViewById(R.id.uri_input);
                String content = edtEditText.getText().toString();
                content = "http://video.ch9.ms/ch9/507d/71f4ef0f-3b81-4d2c-956f-c56c81f9507d/AndroidEmulatorWithMacEmulator.mp4";
                videoPlayer.setVideoPath(content);
            } else {
                String uri = "android.resource://" + getPackageName() + "/" +
                        this.getResources().getIdentifier(item, "raw", this.getPackageName());
                Uri myVideoUri= Uri.parse(uri);
                videoPlayer.setVideoURI(myVideoUri);
            }
            findViewById(R.id.videoPlayer).setVisibility(View.VISIBLE);

            videoPlayer.start();
        } else {
            if (mediaPlayer.isPlaying())
                    return;
            if (item.equals("URL")) {
                EditText edtEditText = findViewById(R.id.uri_input);
                String content = edtEditText.getText().toString();
                content = "http://video.ch9.ms/ch9/507d/71f4ef0f-3b81-4d2c-956f-c56c81f9507d/AndroidEmulatorWithMacEmulator.mp4";
                try {
                    mediaPlayer.setDataSource(content);
                } catch (Exception e){
                    Toast.makeText(getApplicationContext(), "You might not set the URI correctly!", Toast.LENGTH_LONG).show();
                    e.printStackTrace();
                    return;
                }

            } else {
                String uri = "android.resource://" + getPackageName() + "/" +
                        this.getResources().getIdentifier(item, "raw", this.getPackageName());
                Uri myVideoUri= Uri.parse(uri);
                mediaPlayer = MediaPlayer.create(getApplicationContext(), myVideoUri);
            }
            mediaPlayer.start();
        }

        findViewById(R.id.play_btn).setEnabled(false);
        findViewById(R.id.pause_btn).setEnabled(true);
        findViewById(R.id.resume_btn).setEnabled(false);
        findViewById(R.id.stop_btn).setEnabled(true);
    }

    public void pause(View view){
        if (videoIsSelect) {
            videoPlayer.pause();
        } else {
            mediaPlayer.pause();
        }

        findViewById(R.id.play_btn).setEnabled(false);
        findViewById(R.id.pause_btn).setEnabled(false);
        findViewById(R.id.resume_btn).setEnabled(true);
        findViewById(R.id.stop_btn).setEnabled(true);
    }

    public void resume(View view){
        if (videoIsSelect) {
            videoPlayer.start();
        } else {
            mediaPlayer.start();
        }

        findViewById(R.id.play_btn).setEnabled(false);
        findViewById(R.id.pause_btn).setEnabled(true);
        findViewById(R.id.resume_btn).setEnabled(false);
        findViewById(R.id.stop_btn).setEnabled(true);
    }

    public void stop(View view) {
        if (videoIsSelect) {
            videoPlayer.stopPlayback();
            videoPlayer.resume();
        } else {
            mediaPlayer.stop();
            mediaPlayer.seekTo(0);
        }

        findViewById(R.id.play_btn).setEnabled(true);
        findViewById(R.id.pause_btn).setEnabled(false);
        findViewById(R.id.resume_btn).setEnabled(false);
        findViewById(R.id.stop_btn).setEnabled(false);
        findViewById(R.id.videoPlayer).setVisibility(View.GONE);
    }


    public void onRadioButtonClicked(View view) {
        boolean checked = ((RadioButton) view).isChecked();

        switch(view.getId()) {
            case R.id.video_rd_btn:
                if (checked){
                    findViewById(R.id.videoPlayer).setVisibility(View.GONE);

                    releaseMedia();

                    videoIsSelect = true;
                }
                break;
            case R.id.audio_rd_btn:
                if (checked){
                    findViewById(R.id.videoPlayer).setVisibility(View.GONE);

                    videoPlayer.stopPlayback();
                    videoPlayer.resume();

                    videoIsSelect = false;
                }
                break;
        }
    }

    private void releaseMedia(){
        if (mediaPlayer != null) {
            mediaPlayer.release();
            mediaPlayer = null;
        }
    }

    @Override
    protected void onStop() {
        super.onStop();
        if (!videoIsSelect) {
            releaseMedia();
        }
    }
}
