package com.example.lab1;

import androidx.appcompat.app.AppCompatActivity;

import android.os.Bundle;
import android.view.View;
import android.widget.AdapterView;
import android.widget.ArrayAdapter;
import android.widget.Button;
import android.widget.ListView;
import android.widget.Spinner;
import android.widget.Toast;

public class MainActivity extends AppCompatActivity {

    String[] groups = { "", "ІС-71", "ІС-72", "ІС-73" };
    String[] faculties = { "", "ФІОТ", "ФПМ", "ІПСА" };

    String group, faculty;

    private Spinner groupSpinner, facultiesSpinner;

    AdapterView.OnItemSelectedListener groupItemSelectedListener = new AdapterView.OnItemSelectedListener() {
        @Override
        public void onItemSelected(AdapterView<?> parent, View view, int position, long id) {

            group = (String) parent.getItemAtPosition(position);

        }

        @Override
        public void onNothingSelected(AdapterView<?> parent) {

        }
    };

    AdapterView.OnItemSelectedListener facultyItemSelectedListener = new AdapterView.OnItemSelectedListener() {
        @Override
        public void onItemSelected(AdapterView<?> parent, View view, int position, long id) {

            faculty = (String) parent.getItemAtPosition(position);

        }

        @Override
        public void onNothingSelected(AdapterView<?> parent) {

        }
    };

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        groupSpinner = findViewById(R.id.groups);
        facultiesSpinner = findViewById(R.id.faculties);

        ArrayAdapter<String> groupAdapter = new ArrayAdapter(this,
                android.R.layout.simple_spinner_item, groups);
        groupAdapter.setDropDownViewResource(android.R.layout.simple_spinner_dropdown_item);

        ArrayAdapter<String> facultyAdapter = new ArrayAdapter(this,
                android.R.layout.simple_spinner_item, faculties);
        facultyAdapter.setDropDownViewResource(android.R.layout.simple_spinner_dropdown_item);

        groupSpinner.setAdapter(groupAdapter);
        facultiesSpinner.setAdapter(facultyAdapter);

        groupSpinner.setOnItemSelectedListener(groupItemSelectedListener);
        facultiesSpinner.setOnItemSelectedListener(facultyItemSelectedListener);
    }

    public void showMsg(View view) {

        if (group.equals("") || faculty.equals("")) {
            String msg = "Заповніть всі поля!";
            Toast toast = Toast.makeText(this, msg, Toast.LENGTH_LONG);
            toast.show();
        } else {
            String msg = "Факультет: " + faculty + '\n' + "Група: " + group;
            Toast toast = Toast.makeText(this, msg, Toast.LENGTH_LONG);
            toast.show();
        }
    }

    public void setDefault(View view) {
        groupSpinner.setSelection(0);
        facultiesSpinner.setSelection(0);
    }
}
