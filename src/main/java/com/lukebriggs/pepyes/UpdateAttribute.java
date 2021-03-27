package com.lukebriggs.pepyes;

import javax.swing.text.AbstractDocument;
import javax.swing.text.BadLocationException;
import javax.swing.text.SimpleAttributeSet;

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
            abstractDocument.replace(start, length, text, attributeSet);
        } catch (BadLocationException e) {
            e.printStackTrace();
            System.out.println("Start: " + start);
            System.out.println("Length: " + length);
            System.out.println("Text " + text);
        }
    }
}
