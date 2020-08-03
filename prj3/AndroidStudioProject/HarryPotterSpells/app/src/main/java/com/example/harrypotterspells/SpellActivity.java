package com.example.harrypotterspells;

import androidx.appcompat.app.AppCompatActivity;
import androidx.appcompat.widget.AppCompatImageView;

import android.media.RingtoneManager;
import android.net.Uri;
import android.os.Bundle;
import android.provider.MediaStore;
import android.widget.ImageView;
import android.widget.TextView;

public class SpellActivity extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_spell);

        Bundle b = getIntent().getExtras();
        String spell = "";

        if(b != null) {
            spell = b.getString("spell");
        }

        if(spell == null){
            spell = "";
        }
        setupViews(spell);
    }

    private void setupViews(String spell){
        TextView spellText = findViewById(R.id.spellScreenSpell);
        TextView spellTitle = findViewById(R.id.spellScreenMessage);
        AppCompatImageView imageSpell = findViewById(R.id.spellImage);

        if(spell.equals("REVELIO")){
            spellText.setText("REVELIO");
            imageSpell.setImageResource(R.drawable.revelio);
        } else if(spell.equals("ALOHOMORA")) {
            spellText.setText("ALOHOMORA");
            imageSpell.setImageResource(R.drawable.alohomora);
        } else if(spell.equals("ARRESTO_MOMENTUM")) {
            spellText.setText("ARRESTO MOMENTUM");
            imageSpell.setImageResource(R.drawable.arresto_momentum);
        } else if(spell.equals("INCENDIO")) {
            spellText.setText("INCENDIO");
            imageSpell.setImageResource(R.drawable.incendio);
        }else if(spell.equals("WINGARDIUM_LEVIOSA")) {
            spellText.setText("WINGARDIUM LEVIOSA");
            imageSpell.setImageResource(R.drawable.w_leviosa);
        }else if(spell.equals("FINITE_INCANTATEM")) {
            spellText.setText("FINITE INCANTATEM");
            imageSpell.setImageResource(R.drawable.finite_incantatem);
        }else{
            spellTitle.setText("Well, I do not know what it is :(");
            spellText.setText("\"You are not a wizard, Harry\"");
        }
    }
}