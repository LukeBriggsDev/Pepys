package com.lukebriggs.pepyes;

import javax.swing.text.SimpleAttributeSet;
import javax.swing.text.StyleConstants;

public class Emphasis extends AbstractMarkDownBlock{

    boolean bold;
    boolean italics;


    public Emphasis(boolean bold, boolean italics, String regex, boolean regexIsDotAll){
        this.bold = bold;
        this.italics = italics;
        this.regex = regex;
        this.regexIsDotAll = regexIsDotAll;

        StyleConstants.setBold(attributeSet, this.bold);
        StyleConstants.setItalic(attributeSet, this.italics);

    }

    @Override
    SimpleAttributeSet getAttributeSet() {
        return this.attributeSet;
    }

    @Override
    boolean isRegexIsDotAll() {
        return this.regexIsDotAll;
    }

    @Override
    String getRegex() {
        return this.regex;
    }
}
