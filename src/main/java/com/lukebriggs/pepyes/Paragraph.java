package com.lukebriggs.pepyes;

import javax.swing.text.SimpleAttributeSet;
import javax.swing.text.StyleConstants;
import java.awt.*;

public class Paragraph extends AbstractMarkDownBlock {
    int fontSize;
    boolean bold;
    Font font;

    public Paragraph(int fontSize, boolean bold, String fontFamily, String regex, boolean regexIsDotAll) {
        this.regexIsDotAll = regexIsDotAll;
        this.fontSize = fontSize;
        this.regex = regex;
        this.bold = bold;
        this.font = FontParser.parseFont(fontFamily);
        StyleConstants.setFontSize(attributeSet, this.fontSize);
        StyleConstants.setFontFamily(attributeSet, this.font.getFamily());
        StyleConstants.setBold(attributeSet, this.bold);
    }

    public int getFontSize() {
        return fontSize;
    }

    public SimpleAttributeSet getAttributeSet() {
        return attributeSet;
    }

    @Override
    boolean isRegexIsDotAll() {
        return regexIsDotAll;
    }

    public String getRegex() {
        return regex;
    }
}
