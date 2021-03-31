package com.lukebriggs.pepyes;

import javax.swing.*;
import javax.swing.text.*;

public class UpdateAttribute implements  Runnable{
    static boolean ALREADY_PERFORMED = false;
// TODO WEIRD BUG WHEN USING ITALICS IN HEADER#
    AbstractDocument abstractDocument;
    int start;
    int length;
    String text;
    SimpleAttributeSet attributeSet;
    JTextPane textPane;
    char nextChar;

    public UpdateAttribute(AbstractDocument abstractDocument, int start, int length, String text, SimpleAttributeSet attributeSet, JTextPane textPane, char nextChar){
        this.abstractDocument = abstractDocument;
        this.start = start;
        this.length = length;
        this.text = text;
        this.attributeSet = attributeSet;
        this.textPane = textPane;
        this.nextChar = nextChar;
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
            int currentCaretPosition = textPane.getCaretPosition();
            abstractDocument.replace(start, length, text, attributeSet);
            textPane.setCaretPosition(currentCaretPosition);

        } catch (BadLocationException e) {
            e.printStackTrace();
            System.out.println("Start: " + start);
            System.out.println("Length: " + length);
            System.out.println("Text " + text);
        }
    }
}
