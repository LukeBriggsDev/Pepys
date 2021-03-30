package com.lukebriggs.pepyes;

import javax.swing.text.*;

public class UpdateAttribute implements  Runnable{

    AbstractDocument abstractDocument;
    int start;
    int length;
    String text;
    SimpleAttributeSet attributeSet;

    public UpdateAttribute(AbstractDocument abstractDocument, int start, int length, String text, SimpleAttributeSet attributeSet){
        this.abstractDocument = abstractDocument;
        this.start = start;
        this.length = length;
        this.text = text;
        this.attributeSet = attributeSet;
    }

    @Override
    public void run() {
        try {
            if(StyleConstants.isItalic(attributeSet)){
                AttributeSet currentAttributeSet = ((StyledDocument) abstractDocument).getCharacterElement(start).getAttributes();
                StyleConstants.setFontSize(attributeSet, StyleConstants.getFontSize(currentAttributeSet));
                StyleConstants.setFontFamily(attributeSet, StyleConstants.getFontFamily(currentAttributeSet));
                StyleConstants.setItalic(attributeSet, true);
            }
            if(StyleConstants.isBold(attributeSet)){
                AttributeSet currentAttributeSet = ((StyledDocument) abstractDocument).getCharacterElement(start).getAttributes();
                StyleConstants.setFontSize(attributeSet, StyleConstants.getFontSize(currentAttributeSet));
                StyleConstants.setFontFamily(attributeSet, StyleConstants.getFontFamily(currentAttributeSet));
                StyleConstants.setBold(attributeSet, true);
            }

            abstractDocument.replace(start, length, text, attributeSet);
        } catch (BadLocationException e) {
            e.printStackTrace();
            System.out.println("Start: " + start);
            System.out.println("Length: " + length);
            System.out.println("Text " + text);
        }
    }
}
