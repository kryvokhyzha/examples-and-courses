package com.example.lab2;

import android.app.Activity;
import android.content.Context;
import android.os.Bundle;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.Button;

import android.app.Fragment;

public class ButtonFragment extends Fragment implements View.OnClickListener {

    private OnButtonFragmentInteractionListener mListener;

    @Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container,
                             Bundle savedInstanceState) {
        View view = inflater.inflate(R.layout.fragment_button, container, false);

        final Button ok_btn = view.findViewById(R.id.ok_btn);
        ok_btn.setOnClickListener(this);

        final Button cancel_btn = view.findViewById(R.id.cancel_btn);
        cancel_btn.setOnClickListener(this);

        return view;
    }

    interface OnButtonFragmentInteractionListener {
        void onOkClick();
        void onCancelClick();
    }

    @Override
    public void onAttach(Activity MainActivity) {
        super.onAttach(MainActivity);
        mListener = (OnButtonFragmentInteractionListener) MainActivity;
    }

    @Override
    public void onClick(View v) {
        switch (v.getId()) {

            case R.id.ok_btn:
                mListener.onOkClick();
                break;

            case R.id.cancel_btn:
                mListener.onCancelClick();
                break;
        }
    }
}
