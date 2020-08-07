package com.example.harrypotterspells;

import androidx.appcompat.app.AppCompatActivity;

import android.content.Intent;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;

import com.google.android.material.textfield.TextInputEditText;

public class SetupActivity extends AppCompatActivity {

    private String SERVER_ADDRESS = "";

    private TextInputEditText serverAddressInputText;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);


        setContentView(R.layout.activity_setup);

        Button nextButton = findViewById(R.id.nextButton);
        serverAddressInputText = findViewById(R.id.serverAddressInputText);

        nextButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                nextActivity();
            }
        });

        if (!SERVER_ADDRESS.equals("")) {
            serverAddressInputText.setText(SERVER_ADDRESS);
            nextActivity();
        }
    }


    private void nextActivity(){
        Intent intent = new Intent(SetupActivity.this, MainActivity.class);

        Bundle b = new Bundle();
        b.putString("serverAddress", serverAddressInputText.getText().toString());

        intent.putExtras(b); //Put your id to your next Intent
        startActivity(intent);
    }
}