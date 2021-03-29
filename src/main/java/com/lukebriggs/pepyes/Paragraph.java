package com.lukebriggs.pepyes;

import javax.swing.text.SimpleAttributeSet;
import javax.swing.text.StyleConstants;

public class Paragraph extends AbstractMarkDownBlock {
    int fontSize;

    public Paragraph(int fontSize, String regex) {
        this.fontSize = fontSize;
        this.regex = regex;
        StyleConstants.setFontSize(attributeSet, this.fontSize);
    }

    public int getFontSize() {
        return fontSize;
    }

    public SimpleAttributeSet getAttributeSet() {
        return attributeSet;
    }

    public String getRegex() {
        return regex;
    }
}
