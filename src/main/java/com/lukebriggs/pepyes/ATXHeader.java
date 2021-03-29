package com.lukebriggs.pepyes;

import javax.swing.text.StyleConstants;

public class ATXHeader extends AbstractHeader{
    public ATXHeader(int level, int fontSize, boolean bold, String regex, boolean regexIsDotAll) {
        this.level = level;
        this.fontSize = fontSize;
        this.bold = bold;
        this.regex = regex;
        this.regexIsDotAll = regexIsDotAll;
        StyleConstants.setBold(attributeSet, this.bold);
        StyleConstants.setFontSize(attributeSet, this.fontSize);
    }

    @Override
    boolean isRegexIsDotAll() {
        return regexIsDotAll;
    }
}
