package com.lukebriggs.pepyes;

import javax.swing.text.StyleConstants;
import java.awt.*;

public class IndentedCode extends AbstractCode{


    public IndentedCode(int fontSize, boolean bold, Font font, String regex){
        this.fontSize = fontSize;
        this.bold = bold;
        this.font = font;
        this.regex = regex;

        StyleConstants.setFontSize(this.attributeSet, this.fontSize);
        StyleConstants.setBold(this.attributeSet, this.bold);
        StyleConstants.setFontFamily(this.attributeSet, this.font.getFamily());
    }
}
