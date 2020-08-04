package com.example.harrypotterspells;

import androidx.appcompat.app.AppCompatActivity;
import androidx.appcompat.widget.AppCompatImageView;

import android.media.MediaPlayer;
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

            final MediaPlayer mp = MediaPlayer.create(this, R.raw.revelio);
            mp.start();
        } else if(spell.equals("ALOHOMORA")) {
            spellText.setText("ALOHOMORA");
            imageSpell.setImageResource(R.drawable.alohomora);

            final MediaPlayer mp = MediaPlayer.create(this, R.raw.alohomora);
            mp.start();
        } else if(spell.equals("ARRESTO_MOMENTUM")) {
            spellText.setText("ARRESTO MOMENTUM");
            imageSpell.setImageResource(R.drawable.arresto_momentum);

            final MediaPlayer mp = MediaPlayer.create(this, R.raw.arresto_momentum);
            mp.start();
        } else if(spell.equals("INCENDIO")) {
            spellText.setText("INCENDIO");
            imageSpell.setImageResource(R.drawable.incendio);

            final MediaPlayer mp = MediaPlayer.create(this, R.raw.incendio);
            mp.start();
        }else if(spell.equals("WINGARDIUM_LEVIOSA")) {
            spellText.setText("WINGARDIUM LEVIOSA");
            imageSpell.setImageResource(R.drawable.w_leviosa);

            final MediaPlayer mp = MediaPlayer.create(this, R.raw.wingardium_leviosa);
            mp.start();
        }else if(spell.equals("FINITE_INCANTATEM")) {
            spellText.setText("FINITE INCANTATEM");
            imageSpell.setImageResource(R.drawable.finite_incantatem);

            final MediaPlayer mp = MediaPlayer.create(this, R.raw.finite_incantatem);
            mp.start();
        }else{
            spellTitle.setText("Well, I do not know what it is :(");
            spellText.setText("\"You are not a wizard, Harry\"");
        }
    }
}