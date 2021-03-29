package com.lukebriggs.pepyes;

import javax.swing.text.SimpleAttributeSet;

public abstract class AbstractHeader extends AbstractMarkDownBlock {
    int level;
    int fontSize;
    Boolean bold;


    public int getLevel() {
        return level;
    }

    public int getFontSize() {
        return fontSize;
    }

    public String getRegex() {
        return regex;
    }

    public SimpleAttributeSet getAttributeSet() {
        return attributeSet;
    }
}
