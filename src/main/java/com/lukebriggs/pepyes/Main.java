package com.lukebriggs.pepyes;

import javax.swing.*;
import javax.swing.text.AbstractDocument;
import javax.swing.text.BadLocationException;
import javax.swing.text.SimpleAttributeSet;
import java.awt.event.KeyAdapter;
import java.awt.event.KeyEvent;
import java.io.File;
import java.nio.charset.StandardCharsets;
import java.util.Scanner;
import java.util.regex.Matcher;
import java.util.regex.Pattern;


public class Main {
    static String EOL = System.getProperty("line.separator");
    public static void main(String[] args) {
        try {
            if(System.getProperty("os.name").equals("Linux")){
                UIManager.setLookAndFeel("com.sun.java.swing.plaf.gtk.GTKLookAndFeel");
            }
            else {
                // Set System L&F
                UIManager.setLookAndFeel(UIManager.getSystemLookAndFeelClassName());
            }
        } catch (UnsupportedLookAndFeelException e) {
            // handle exception
        }
        catch (ClassNotFoundException e) {
            // handle exception
        }
        catch (InstantiationException e) {
            // handle exception
        }
        catch (IllegalAccessException e) {
            // handle exception
        }
        final MarkDownStyle style;
        MarkDownStyle testStyle;
        ClassLoader classLoader = Main.class.getClassLoader();
        Scanner jsonScanner = new Scanner(classLoader.getResourceAsStream("style.json"), StandardCharsets.UTF_8.name());
        File styleFile = new File("");
        testStyle = new MarkDownStyle(jsonScanner.useDelimiter("\\A").next());
        style = testStyle;

        JFrame frame = new JFrame();
        final JTextPane textPane = new JTextPane();

        SimpleAttributeSet entryAttributeSet = new SimpleAttributeSet();

        textPane.addKeyListener(new KeyAdapter() {
            @Override
            public void keyTyped(KeyEvent e) {

                if (textPane.getDocument().getLength() > 0) {
                    try {
                        boolean atBeginningOfLine;
                        try {
                            atBeginningOfLine = textPane.getDocument().getText(textPane.getDocument().getLength() -1 , 1).equals(EOL);
                        } catch (BadLocationException atStartOfFile) {
                            atBeginningOfLine = true;
                        }

                        if(atBeginningOfLine){
                            textPane.setCharacterAttributes(style.getParagraph().getAttributeSet(), true);
                        }

                        // Apply header styles
                        for (int i = 1; i <= 6; i++) {
                            Pattern headerPattern = Pattern.compile(style.getHeader(i).getRegex(), Pattern.MULTILINE);
                            System.out.println(style.getHeader(i).getRegex());
                            Matcher matcher = headerPattern.matcher(textPane.getDocument().getText(0, textPane.getStyledDocument().getLength()) + e.getKeyChar());
                            while (matcher.find()) {
                                UpdateAttribute updateAttribute = new UpdateAttribute((AbstractDocument) textPane.getDocument(), matcher.start(), matcher.end() - matcher.start(), matcher.group(), style.getHeader(i).getAttributeSet());
                                textPane.setCharacterAttributes(style.getHeader(i).getAttributeSet(), true);
                                SwingUtilities.invokeLater(updateAttribute);

                            }
                        }



                        // Apply paragraph style
                        Pattern paragraphPattern = Pattern.compile(style.getParagraph().getRegex(), Pattern.MULTILINE);
                        Matcher matcher = paragraphPattern.matcher(textPane.getDocument().getText(0, textPane.getStyledDocument().getLength()) + e.getKeyChar());
                        while (matcher.find()) {
                            UpdateAttribute updateAttribute = new UpdateAttribute((AbstractDocument) textPane.getDocument(), matcher.start(), matcher.end() - matcher.start(), matcher.group(), style.getParagraph().getAttributeSet());
                            textPane.setCharacterAttributes(style.getParagraph().getAttributeSet(), true);
                            SwingUtilities.invokeLater(updateAttribute);

                        }


                    } catch (BadLocationException badLocationException) {
                        badLocationException.printStackTrace();
                    }
                }
                else{
                    textPane.setCharacterAttributes(style.getParagraph().getAttributeSet(), true);
                }
            }
        });

        frame.setSize(800,600);
        frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        frame.add(textPane);
        frame.setVisible(true);
    }


}
