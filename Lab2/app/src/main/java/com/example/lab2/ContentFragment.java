package com.example.lab2;

import android.view.View;
import android.view.LayoutInflater;
import android.view.ViewGroup;
import android.os.Bundle;
import android.widget.ArrayAdapter;
import android.widget.Button;
import android.widget.Spinner;
import android.widget.Toast;

import androidx.fragment.app.Fragment;


public class ContentFragment extends Fragment implements View.OnClickListener {

    private Spinner groupSpinner, facultiesSpinner;

    @Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container,
                             Bundle savedInstanceState) {
        View view = inflater.inflate(R.layout.fragment_group, container, false);

        final String[] groups = getResources().getStringArray(R.array.groups);
        final String[] faculties = getResources().getStringArray(R.array.faculties);

        groupSpinner = view.findViewById(R.id.groups);
        facultiesSpinner = view.findViewById(R.id.faculties);

        ArrayAdapter<String> groupAdapter = new ArrayAdapter(getActivity().getBaseContext(),
                android.R.layout.simple_spinner_item, groups);
        groupAdapter.setDropDownViewResource(android.R.layout.simple_spinner_dropdown_item);

        ArrayAdapter<String> facultyAdapter = new ArrayAdapter(getActivity().getBaseContext(),
                android.R.layout.simple_spinner_item, faculties);
        facultyAdapter.setDropDownViewResource(android.R.layout.simple_spinner_dropdown_item);

        groupSpinner.setAdapter(groupAdapter);
        facultiesSpinner.setAdapter(facultyAdapter);

        final Button ok_btn = view.findViewById(R.id.ok_btn);
        ok_btn.setOnClickListener(this);

        final Button cancel_btn = view.findViewById(R.id.cancel_btn);
        cancel_btn.setOnClickListener(this);

        return view;
    }

    @Override
    public void onClick(View v) {
        switch (v.getId()) {

            case R.id.ok_btn:
                String group = groupSpinner.getSelectedItem().toString();
                String faculty = facultiesSpinner.getSelectedItem().toString();

                if (group.equals("") || faculty.equals("")) {
                    String msg = "Заповніть всі поля!";
                    Toast toast = Toast.makeText(getActivity(), msg, Toast.LENGTH_SHORT);
                    toast.show();
                } else {
                    String msg = "Факультет: " + faculty + '\n' + "Група: " + group;
                    Toast toast = Toast.makeText(getActivity(), msg, Toast.LENGTH_SHORT);
                    toast.show();
                }
                break;

            case R.id.cancel_btn:
                groupSpinner.setSelection(0);
                facultiesSpinner.setSelection(0);
                break;
        }
    }
}
