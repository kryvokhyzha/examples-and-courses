package com.example.lab2;

import android.os.Bundle;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ArrayAdapter;
import android.widget.Spinner;

import android.app.Fragment;

public class GroupFragment extends Fragment {

    private Spinner groupSpinner;

    @Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container,
                             Bundle savedInstanceState) {
        View view = inflater.inflate(R.layout.fragment_group, container, false);

        final String[] groups = getResources().getStringArray(R.array.groups);

        groupSpinner = view.findViewById(R.id.groups);

        ArrayAdapter<String> groupAdapter = new ArrayAdapter(getActivity().getBaseContext(),
                android.R.layout.simple_spinner_item, groups);
        groupAdapter.setDropDownViewResource(android.R.layout.simple_spinner_dropdown_item);

        groupSpinner.setAdapter(groupAdapter);

        return view;
    }

    public String getGroup(){
        return groupSpinner.getSelectedItem().toString();
    }

    public void setSelection() {
        groupSpinner.setSelection(0);
    }
}
