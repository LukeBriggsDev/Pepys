package com.lukebriggs.pepyes;

import javax.swing.*;
import javax.swing.text.AbstractDocument;
import javax.swing.text.BadLocationException;
import javax.swing.text.SimpleAttributeSet;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

public abstract class AbstractMarkDownBlock {
    SimpleAttributeSet attributeSet = new SimpleAttributeSet();
    String regex;
    boolean regexIsDotAll;

    public void applyStyle(JTextPane textPane, SimpleAttributeSet paragraphAttrSet,char nextChar) throws BadLocationException {
        Pattern headerPattern = Pattern.compile(this.regex, this.regexIsDotAll ? Pattern.MULTILINE | Pattern.DOTALL : Pattern.MULTILINE);
        System.out.println(this.regex);
        Matcher matcher = headerPattern.matcher(textPane.getDocument().getText(0, textPane.getStyledDocument().getLength()) + nextChar);
        while (matcher.find()) {
            UpdateAttribute updateAttribute = new UpdateAttribute((AbstractDocument) textPane.getDocument(), matcher.start(), matcher.end() - matcher.start(), matcher.group(), this.getAttributeSet());
            textPane.setCharacterAttributes(this.getAttributeSet(), true);
            SwingUtilities.invokeLater(updateAttribute);

        }
        textPane.setCharacterAttributes(paragraphAttrSet, false);
    }

    abstract SimpleAttributeSet getAttributeSet();

    abstract boolean isRegexIsDotAll();

    abstract String getRegex();
}
