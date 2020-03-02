package com.example.lab2;

import androidx.appcompat.app.AppCompatActivity;

import android.os.Bundle;
import android.widget.Toast;


public class MainActivity extends AppCompatActivity implements ButtonFragment.OnButtonFragmentInteractionListener {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
    }

    @Override
    public void onOkClick() {
        FacultyFragment facultyFragment = (FacultyFragment) getFragmentManager()
                .findFragmentById(R.id.facultyFragment);

        GroupFragment groupFragment = (GroupFragment) getFragmentManager()
                .findFragmentById(R.id.groupFragment);

        if (facultyFragment != null && facultyFragment.isInLayout() &&
                groupFragment != null && groupFragment.isInLayout()) {

            String faculty = facultyFragment.getFaculty();
            String group = groupFragment.getGroup();

            show_msg(faculty, group);
        }
    }

    @Override
    public void onCancelClick() {
        FacultyFragment facultyFragment = (FacultyFragment) getFragmentManager()
                .findFragmentById(R.id.facultyFragment);

        GroupFragment groupFragment = (GroupFragment) getFragmentManager()
                .findFragmentById(R.id.groupFragment);

        if (facultyFragment != null && facultyFragment.isInLayout() &&
                groupFragment != null && groupFragment.isInLayout()) {

            facultyFragment.setSelection();
            groupFragment.setSelection();
        }
    }

    private void show_msg(String faculty, String group) {
        if (group.equals("") || faculty.equals("")) {
            String msg = "Заповніть всі поля!";
            Toast toast = Toast.makeText(this, msg, Toast.LENGTH_SHORT);
            toast.show();
        } else {
            String msg = "Факультет: " + faculty + '\n' + "Група: " + group;
            Toast toast = Toast.makeText(this, msg, Toast.LENGTH_SHORT);
            toast.show();
        }
    }
}
