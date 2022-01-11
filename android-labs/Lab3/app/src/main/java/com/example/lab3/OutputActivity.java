package com.example.lab3;

import androidx.appcompat.app.AppCompatActivity;

import android.os.Bundle;
import android.widget.TextView;

import java.util.ArrayList;

public class OutputActivity extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_output);

        ArrayList<String> allRecords = getIntent().getStringArrayListExtra("allRecords");

        final TextView outputTextView = findViewById(R.id.output);

        StringBuilder result = new StringBuilder();
        assert allRecords != null;

        if (allRecords.size() > 0) {
            for (String e: allRecords) {
                result.append(e);
            }
        } else {
            String empty_table_msg = getResources().getString(R.string.empty_table_msg);
            result.append(empty_table_msg);
        }



        outputTextView.setText(result);
    }
}
