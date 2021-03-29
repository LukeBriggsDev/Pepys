package com.lukebriggs.pepyes;

import com.google.gson.JsonObject;
import com.google.gson.JsonParser;

import javax.swing.*;
import javax.swing.text.SimpleAttributeSet;
import javax.swing.text.StyleConstants;

public class MarkDownStyle {

    private Header[] headers = new Header[6];
    private Paragraph paragraph;

    public MarkDownStyle(String style){
        JsonObject jsonStyle = new JsonParser().parse(style).getAsJsonObject();

        for(int i=0; i < 6; i++){
            this.headers[i] = new Header(
                jsonStyle.get("header" + String.valueOf(i + 1)).getAsJsonObject().get("level").getAsInt(),
                jsonStyle.get("header" + String.valueOf(i + 1)).getAsJsonObject().get("fontSize").getAsInt(),
                jsonStyle.get("header" + String.valueOf(i + 1)).getAsJsonObject().get("bold").getAsBoolean(),
                    jsonStyle.get("header" + String.valueOf(i + 1)).getAsJsonObject().get("regex").getAsString());
        }

        this.paragraph = new Paragraph(
                jsonStyle.get("paragraph").getAsJsonObject().get("fontSize").getAsInt(),
                jsonStyle.get("paragraph").getAsJsonObject().get("regex").getAsString()
        );
    }

    public Paragraph getParagraph(){
        return paragraph;
    }

    public Header getHeader(int i) {
        return headers[i - 1];
    }

    public void setParagraphStyle(SimpleAttributeSet attributeSet, JTextPane textPane){
        StyleConstants.setBold(attributeSet, false);
        StyleConstants.setFontSize(attributeSet, 16);
    }
}


