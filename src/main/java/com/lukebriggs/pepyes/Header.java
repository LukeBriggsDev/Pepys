package com.lukebriggs.pepyes;

import javax.swing.text.SimpleAttributeSet;
import javax.swing.text.StyleConstants;

public class Header extends AbstractMarkDownBlock {
    int level;
    int fontSize;
    Boolean bold;

    public Header(int level, int fontSize, boolean bold, String regex) {
        this.level = level;
        this.fontSize = fontSize;
        this.bold = bold;
        this.regex = regex;
        StyleConstants.setBold(attributeSet, this.bold);
        StyleConstants.setFontSize(attributeSet, this.fontSize);
    }


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
