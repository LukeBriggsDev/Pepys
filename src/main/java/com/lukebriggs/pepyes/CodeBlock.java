package com.lukebriggs.pepyes;

import javax.swing.text.StyleConstants;

public class CodeBlock extends AbstractCode{
    public CodeBlock(int fontSize, boolean bold, boolean italics, String font, String regex, boolean regexIsDotAll){
        this.fontSize = fontSize;
        this.bold = bold;
        this.font = FontParser.parseFont(font);
        this.regex = regex;
        this.regexIsDotAll = regexIsDotAll;
        this.italics = italics;

        StyleConstants.setFontSize(this.attributeSet, this.fontSize);
        StyleConstants.setBold(this.attributeSet, this.bold);
        StyleConstants.setItalic(this.attributeSet, this.italics);
        StyleConstants.setFontFamily(this.attributeSet, this.font.getFamily());
    }

    @Override
    boolean isRegexIsDotAll() {
        return regexIsDotAll;
    }
}
