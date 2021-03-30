package com.lukebriggs.pepyes;

import javax.swing.*;
import javax.swing.text.*;

public class CustomTextPane extends JTextPane {
    private boolean lineWrap;

    public CustomTextPane(final boolean lineWrap) {
        this.lineWrap = lineWrap;

        if (lineWrap)
            setEditorKit(new WrapEditorKit());
    }

    @Override
    public boolean getScrollableTracksViewportWidth() {
        if (lineWrap)
            return super.getScrollableTracksViewportWidth();
        else
            return getParent() == null
                    || getUI().getPreferredSize(this).width <= getParent().getSize().width;
    }

    private class WrapEditorKit extends StyledEditorKit {
        private final ViewFactory defaultFactory = new WrapColumnFactory();

        @Override
        public ViewFactory getViewFactory() {
            return defaultFactory;
        }
    }

    private class WrapColumnFactory implements ViewFactory {
        @Override
        public View create(final Element element) {
            final String kind = element.getName();
            if (kind != null) {
                switch (kind) {
                    case AbstractDocument.ContentElementName:
                        return new WrapLabelView(element);
                    case AbstractDocument.ParagraphElementName:
                        return new ParagraphView(element);
                    case AbstractDocument.SectionElementName:
                        return new BoxView(element, View.Y_AXIS);
                    case StyleConstants.ComponentElementName:
                        return new ComponentView(element);
                    case StyleConstants.IconElementName:
                        return new IconView(element);
                }
            }

            // Default to text display.
            return new LabelView(element);
        }
    }

    private class WrapLabelView extends LabelView {
        public WrapLabelView(final Element element) {
            super(element);
        }

        @Override
        public float getMinimumSpan(final int axis) {
            switch (axis) {
                case View.X_AXIS:
                    return 0;
                case View.Y_AXIS:
                    return super.getMinimumSpan(axis);
                default:
                    throw new IllegalArgumentException("Invalid axis: " + axis);
            }
        }
    }
}