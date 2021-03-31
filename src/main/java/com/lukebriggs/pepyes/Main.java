package com.lukebriggs.pepyes;

import javax.swing.*;
import javax.swing.event.CaretEvent;
import javax.swing.event.CaretListener;
import javax.swing.text.BadLocationException;
import java.awt.*;
import java.awt.event.KeyAdapter;
import java.awt.event.KeyEvent;
import java.nio.charset.StandardCharsets;
import java.util.Objects;
import java.util.Scanner;


public class Main {
    static String EOL = System.getProperty("line.separator");
    static int currentCaretPosition = 0;

    public static void main(String[] args) {
        try {
            if(System.getProperty("os.name").equals("Linux")){
                UIManager.setLookAndFeel("com.sun.java.swing.plaf.gtk.GTKLookAndFeel");
            }
            else {
                // Set System L&F
                UIManager.setLookAndFeel(UIManager.getSystemLookAndFeelClassName());
            }
        } catch (UnsupportedLookAndFeelException | ClassNotFoundException | InstantiationException | IllegalAccessException e) {
            // handle exception
        }

        final MarkDownStyle style;
        MarkDownStyle testStyle;
        ClassLoader classLoader = Main.class.getClassLoader();
        Scanner jsonScanner = new Scanner(Objects.requireNonNull(classLoader.getResourceAsStream("style.json")), StandardCharsets.UTF_8.name());
        testStyle = new MarkDownStyle(jsonScanner.useDelimiter("\\A").next());
        style = testStyle;

        JFrame frame = new JFrame();
        final CustomTextPane textPane = new CustomTextPane(true);
        textPane.setFont(FontParser.parseFont("SystemSansSerif"));

        frame.setSize(800,600);
        frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        JScrollPane scrollPaneText = new JScrollPane(textPane);
        scrollPaneText.setVerticalScrollBarPolicy(ScrollPaneConstants.VERTICAL_SCROLLBAR_AS_NEEDED);
        frame.getContentPane().add(scrollPaneText, BorderLayout.CENTER);
        frame.setVisible(true);

        textPane.addCaretListener(new CaretListener() {
            @Override
            public void caretUpdate(CaretEvent e) {
            }
        });



        textPane.addKeyListener(new KeyAdapter() {
            @Override
            public void keyTyped(KeyEvent e) {
                System.out.println("Hi");

                currentCaretPosition = textPane.getCaretPosition();

                if (textPane.getDocument().getLength() > 0 && e.getKeyChar() != 8) {
                    try {
                        boolean atBeginningOfLine;
                        try {
                            textPane.getDocument().insertString(textPane.getCaretPosition(), String.valueOf(e.getKeyChar()), textPane.getCharacterAttributes());
                            atBeginningOfLine = textPane.getDocument().getText(textPane.getDocument().getLength() -1 , 1).equals(EOL);
                        } catch (BadLocationException atStartOfFile) {
                            atBeginningOfLine = true;
                        }


                        if(atBeginningOfLine){
                            textPane.setCharacterAttributes(style.getParagraph().getAttributeSet(), true);
                        }

                        // Apply atx header styles
                        for (int i = 1; i <= 6; i++) {
                            style.getAtxHeader(i).applyStyle(textPane, style.getParagraph().getAttributeSet(), e.getKeyChar());
                        }

                        for (int i = 1; i <= 2; i++) {
                            style.getSetextHeader(i).applyStyle(textPane, style.getParagraph().getAttributeSet(), e.getKeyChar());
                        }


                        // Apply emphasis
                        style.getEmphasis().applyStyle(textPane, style.getParagraph().getAttributeSet(), e.getKeyChar());

                        // Apply strong emphasis
                        style.getStrongEmphasis().applyStyle(textPane, style.getParagraph().getAttributeSet(), e.getKeyChar());

                        // Apply indented code style
                        style.getIndentedCode().applyStyle(textPane, style.getParagraph().getAttributeSet(), e.getKeyChar());

                        // Apply Code block style
                        style.getCodeBlock().applyStyle(textPane, style.getParagraph().getAttributeSet(), e.getKeyChar());

                        UpdateAttribute.ALREADY_PERFORMED = false;

                        System.out.println(textPane.getCaretPosition());

                        if(textPane.getDocument().getLength() > 1) {

                            if(textPane.getCaretPosition() < textPane.getDocument().getLength()) {
                                textPane.setCaretPosition(textPane.getCaretPosition() - 1);
                            }

                            textPane.getDocument().remove(textPane.getDocument().getLength() - 1, 1);

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

    }


}
