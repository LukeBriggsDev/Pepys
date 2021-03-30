package com.lukebriggs.pepyes;

import javax.swing.text.StyleConstants;

public class IndentedCode extends AbstractCode{


    public IndentedCode(int fontSize, boolean bold, boolean italics, String font, String regex, boolean regexIsDotAll){
        this.fontSize = fontSize;
        this.bold = bold;
        this.italics = italics;
        this.font = FontParser.parseFont(font);
        this.regex = regex;
        this.regexIsDotAll = regexIsDotAll;

        StyleConstants.setFontSize(this.attributeSet, this.fontSize);
        StyleConstants.setBold(this.attributeSet, this.bold);
        StyleConstants.setFontFamily(this.attributeSet, this.font.getFamily());
    }

    @Override
    boolean isRegexIsDotAll() {
        return regexIsDotAll;
    }
}
