package com.example.lab3;

import androidx.appcompat.app.AppCompatActivity;

import android.content.ContentValues;
import android.content.Intent;
import android.database.Cursor;
import android.database.sqlite.SQLiteDatabase;
import android.os.Bundle;
import android.view.View;
import android.widget.ArrayAdapter;
import android.widget.Spinner;
import android.widget.Toast;

import java.util.ArrayList;
import java.util.List;

public class MainActivity extends AppCompatActivity {

    private Spinner groupSpinner, facultiesSpinner;


    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        final String[] groups = getResources().getStringArray(R.array.groups);
        final String[] faculties = getResources().getStringArray(R.array.faculties);

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
    }

    // сохранение состояния
    @Override
    protected void onSaveInstanceState(Bundle savedInstanceState) {
        super.onSaveInstanceState(savedInstanceState);

        savedInstanceState.putInt("groupSpinnerPosition", groupSpinner.getSelectedItemPosition());
        savedInstanceState.putInt("facultySpinnerPosition", facultiesSpinner.getSelectedItemPosition());
    }

    // получение ранее сохраненного состояния
    @Override
    protected void onRestoreInstanceState(Bundle savedInstanceState) {
        super.onRestoreInstanceState(savedInstanceState);

        groupSpinner.setSelection(savedInstanceState.getInt("groupSpinnerPosition"));
        groupSpinner.setSelection(savedInstanceState.getInt("facultySpinnerPosition"));
    }

    public void showMsg(View view) {

        String group = groupSpinner.getSelectedItem().toString();
        String faculty = facultiesSpinner.getSelectedItem().toString();

        if (group.equals("") || faculty.equals("")) {
            String msg = getResources().getString(R.string.fill_all_fields_msg);
            Toast toast = Toast.makeText(this, msg, Toast.LENGTH_SHORT);
            toast.show();
        } else {
            insertRecord(group, faculty);

            String msg = getResources().getString(R.string.save_record_msg);
            Toast toast = Toast.makeText(this, msg, Toast.LENGTH_SHORT);
            toast.show();
        }
    }

    public void insertRecord(String group, String faculty) {
        String db_name = getResources().getString(R.string.db_name);

        SQLiteDatabase db = getBaseContext().openOrCreateDatabase(db_name, MODE_PRIVATE, null);

        String records_table_name = getResources().getString(R.string.records_table_name);
        String create_table = getResources().getString(R.string.create_table);
        String group_column_name = getResources().getString(R.string.group_column_name);
        String faculty_column_name = getResources().getString(R.string.faculty_column_name);

        ContentValues cv = new ContentValues();
        cv.put(group_column_name, group);
        cv.put(faculty_column_name, faculty);

        db.execSQL(String.format(create_table, records_table_name, group_column_name, faculty_column_name));
        db.insert(records_table_name, null, cv);

        db.close();
    }

    public List<String> getAllRecords() {
        List<String> allRecords = new ArrayList<>();
        String db_name = getResources().getString(R.string.db_name);

        SQLiteDatabase db = getBaseContext().openOrCreateDatabase(db_name, MODE_PRIVATE, null);

        String select_all_from_table = getResources().getString(R.string.select_all_from_table);
        String records_table_name = getResources().getString(R.string.records_table_name);

        Cursor query = db.rawQuery(String.format(select_all_from_table, records_table_name), null);
        if(query.moveToFirst()){
            do {
                int id = query.getInt(0);
                String group = query.getString(1);
                String faculty = query.getString(2);

                allRecords.add(id + ". Group: " + group + "; Faculty: " + faculty + "\n");
            } while(query.moveToNext());
        }

        query.close();
        db.close();

        return allRecords;
    }

    public void setDefault(View view) {
        groupSpinner.setSelection(0);
        facultiesSpinner.setSelection(0);
    }

    public void showRecords(View view) {
        Intent intent = new Intent(this, OutputActivity.class);

        intent.putStringArrayListExtra("allRecords", (ArrayList<String>) getAllRecords());

        startActivity(intent);
    }

    public void clearTable(View view) {
        String db_name = getResources().getString(R.string.db_name);

        SQLiteDatabase db = getBaseContext().openOrCreateDatabase(db_name, MODE_PRIVATE, null);

        String records_table_name = getResources().getString(R.string.records_table_name);
        String delete_from_table = getResources().getString(R.string.delete_from_table);

        db.execSQL(String.format(delete_from_table, records_table_name));

        db.close();
    }
}
