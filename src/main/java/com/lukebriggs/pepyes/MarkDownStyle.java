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
                jsonStyle.get("header" + String.valueOf(i + 1)).getAsJsonObject().get("bold").getAsBoolean());
        }

        this.paragraph = new Paragraph(
                jsonStyle.get("paragraph").getAsJsonObject().get("fontSize").getAsInt()
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


class Header{
    int level;
    int fontSize;
    Boolean bold;
    SimpleAttributeSet attributeSet = new SimpleAttributeSet();

    public Header(int level, int fontSize, boolean bold){
        this.level = level;
        this.fontSize = fontSize;
        this.bold = bold;
        StyleConstants.setBold(attributeSet, this.bold);
        StyleConstants.setFontSize(attributeSet, this.fontSize);
    }

    public int getLevel() {
        return level;
    }
    public int getFontSize(){
        return fontSize;
    }

    public SimpleAttributeSet getAttributeSet() {
        return attributeSet;
    }
}

class Paragraph{
    int fontSize;
    SimpleAttributeSet attributeSet = new SimpleAttributeSet();

    public Paragraph(int fontSize){
        this.fontSize = fontSize;
        StyleConstants.setFontSize(attributeSet, this.fontSize);
    }

    public int getFontSize() {
        return fontSize;
    }

    public SimpleAttributeSet getAttributeSet() {
        return attributeSet;
    }
}
