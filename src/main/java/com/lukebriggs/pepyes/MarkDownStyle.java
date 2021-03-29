package com.lukebriggs.pepyes;

import com.google.gson.JsonObject;
import com.google.gson.JsonParser;

import javax.swing.*;
import javax.swing.text.SimpleAttributeSet;
import javax.swing.text.StyleConstants;
import java.awt.*;

public class MarkDownStyle {

    private ATXHeader[] atxHeaders = new ATXHeader[6];
    private SetextHeader[] setextHeaders = new SetextHeader[2];
    private IndentedCode indentedCode;
    private Paragraph paragraph;

    public MarkDownStyle(String style){
        JsonObject jsonStyle = new JsonParser().parse(style).getAsJsonObject();

        for(int i=1; i <= 6; i++){
            this.atxHeaders[i - 1] = new ATXHeader(
                jsonStyle.get("atxheader" + String.valueOf(i)).getAsJsonObject().get("level").getAsInt(),
                jsonStyle.get("atxheader" + String.valueOf(i)).getAsJsonObject().get("fontSize").getAsInt(),
                jsonStyle.get("atxheader" + String.valueOf(i)).getAsJsonObject().get("bold").getAsBoolean(),
                    jsonStyle.get("atxheader" + String.valueOf(i)).getAsJsonObject().get("regex").getAsString());
        }

        for(int i=1; i<=2; i++){
            this.setextHeaders[i-1] = new SetextHeader(
                    jsonStyle.get("setextheader" + String.valueOf(i)).getAsJsonObject().get("level").getAsInt(),
                    jsonStyle.get("setextheader" + String.valueOf(i)).getAsJsonObject().get("fontSize").getAsInt(),
                    jsonStyle.get("setextheader" + String.valueOf(i)).getAsJsonObject().get("bold").getAsBoolean(),
                    jsonStyle.get("setextheader" + String.valueOf(i)).getAsJsonObject().get("regex").getAsString());
        }

        this.indentedCode = new IndentedCode(
                jsonStyle.get("indentedcode").getAsJsonObject().get("fontSize").getAsInt(),
                jsonStyle.get("indentedcode").getAsJsonObject().get("bold").getAsBoolean(),
                new Font(jsonStyle.get("indentedcode").getAsJsonObject().get("font").getAsString(), Font.PLAIN, 16),
                jsonStyle.get("indentedcode").getAsJsonObject().get("regex").getAsString()
        );

        this.paragraph = new Paragraph(
                jsonStyle.get("paragraph").getAsJsonObject().get("fontSize").getAsInt(),
                jsonStyle.get("paragraph").getAsJsonObject().get("regex").getAsString()
        );
    }

    public Paragraph getParagraph(){
        return paragraph;
    }

    public ATXHeader getAtxHeader(int i) {
        return atxHeaders[i - 1];
    }

    public SetextHeader getSetextHeader(int i) {
        return setextHeaders[i - 1];
    }

    public IndentedCode getIndentedCode() {
        return indentedCode;
    }

    public void setParagraphStyle(SimpleAttributeSet attributeSet, JTextPane textPane){
        StyleConstants.setBold(attributeSet, false);
        StyleConstants.setFontSize(attributeSet, 16);
    }
}


