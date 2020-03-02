package com.example.lab2;

import android.os.Bundle;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ArrayAdapter;
import android.widget.Spinner;

import android.app.Fragment;

public class FacultyFragment extends Fragment {

    private Spinner facultiesSpinner;

    @Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container,
                             Bundle savedInstanceState) {
        View view = inflater.inflate(R.layout.fragment_faculty, container, false);

        final String[] faculties = getResources().getStringArray(R.array.faculties);

        facultiesSpinner = view.findViewById(R.id.faculties);

        ArrayAdapter<String> facultyAdapter = new ArrayAdapter(getActivity().getBaseContext(),
                android.R.layout.simple_spinner_item, faculties);
        facultyAdapter.setDropDownViewResource(android.R.layout.simple_spinner_dropdown_item);

        facultiesSpinner.setAdapter(facultyAdapter);

        return view;
    }

    public String getFaculty() {
        return facultiesSpinner.getSelectedItem().toString();
    }

    public void setSelection() {
        facultiesSpinner.setSelection(0);
    }
}
