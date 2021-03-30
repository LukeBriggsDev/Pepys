package com.lukebriggs.pepyes;

import javax.swing.text.SimpleAttributeSet;
import java.awt.*;

public abstract class AbstractCode extends AbstractMarkDownBlock{

    int fontSize;
    boolean bold;
    boolean italics;
    Font font;

    @Override
    SimpleAttributeSet getAttributeSet() {
        return attributeSet;
    }

    @Override
    String getRegex() {
        return regex;
    }
}
