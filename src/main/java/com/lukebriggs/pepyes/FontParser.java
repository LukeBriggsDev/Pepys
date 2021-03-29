package com.lukebriggs.pepyes;


import java.awt.*;
import java.util.ArrayList;
import java.util.Arrays;

public class FontParser {
    static ArrayList<String> systemFonts = new ArrayList<>(Arrays.asList(GraphicsEnvironment.getLocalGraphicsEnvironment().getAvailableFontFamilyNames()));
    public static Font parseFont(String fontFamily) {



        Font font = null;


        switch (fontFamily) {
            case "SystemMonospace":
                if (System.getProperty("os.name").equals("Linux") && systemFonts.contains("Liberation Mono")) {
                    font = new Font("Liberation Mono", Font.PLAIN, 16);

                } else if (System.getProperty("os.name").equals("Windows 10") && systemFonts.contains("Consolas")) {
                    font = new Font("Consolas", Font.PLAIN, 16);

                } else if (System.getProperty("os.name").equals("Windows 8.1") && systemFonts.contains("Consolas")) {
                    font = new Font("Consolas", Font.PLAIN, 16);

                } else if (System.getProperty("os.name").equals("Windows 8") && systemFonts.contains("Consolas")) {
                    font = new Font("Consolas", Font.PLAIN, 16);

                } else if (System.getProperty("os.name").equals("Windows 7") && systemFonts.contains("Consolas")) {
                    font = new Font("Consolas", Font.PLAIN, 16);

                } else if (System.getProperty("os.name").equals("Mac OS X") && systemFonts.contains("SF Mono")) {
                    font = new Font("SF Mono", Font.PLAIN, 16);

                } else {
                    font = new Font("Monospaced", Font.PLAIN, 16);
                }
                break;

            case "SystemSansSerif":
                if (System.getProperty("os.name").equals("Linux") && systemFonts.contains("Nimbus Sans")) {
                    font = new Font("Nimbus Sans", Font.PLAIN, 16);

                } else if (System.getProperty("os.name").equals("Windows 10") && systemFonts.contains("Segoe UI")) {
                    font = new Font("Segoe UI", Font.PLAIN, 16);

                } else if (System.getProperty("os.name").equals("Windows 8.1") && systemFonts.contains("Segoe UI")) {
                    font = new Font("Segoe UI", Font.PLAIN, 16);

                } else if (System.getProperty("os.name").equals("Windows 8") && systemFonts.contains("Segoe UI")) {
                    font = new Font("Segoe UI", Font.PLAIN, 16);

                } else if (System.getProperty("os.name").equals("Windows 7") && systemFonts.contains("Segoe UI")) {
                    font = new Font("Segoe UI", Font.PLAIN, 16);

                } else if (System.getProperty("os.name").equals("Mac OS X") && systemFonts.contains("San Francisco")) {
                    font = new Font("San Francisco", Font.PLAIN, 16);

                } else {
                    font = new Font("SansSerif", Font.PLAIN, 16);
                }
                break;

            default:
                font = new Font("SansSerif", Font.PLAIN, 16);

        }
        return font;
    }

}
