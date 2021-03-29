package com.lukebriggs.pepyes;

import javax.swing.text.SimpleAttributeSet;
import java.awt.*;

public abstract class AbstractCode extends AbstractMarkDownBlock{

    int fontSize;
    Boolean bold;
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
