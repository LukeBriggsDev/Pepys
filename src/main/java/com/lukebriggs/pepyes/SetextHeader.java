package com.lukebriggs.pepyes;

import javax.swing.text.StyleConstants;

public class SetextHeader extends AbstractHeader{
    public SetextHeader(int level, int fontSize, String regex, boolean regexIsDotAll) {
        this.level = level;
        this.fontSize = fontSize;
        this.regex = regex;
        this.regexIsDotAll = regexIsDotAll;
        StyleConstants.setFontSize(attributeSet, this.fontSize);
    }

    @Override
    boolean isRegexIsDotAll() {
        return regexIsDotAll;
    }
}
