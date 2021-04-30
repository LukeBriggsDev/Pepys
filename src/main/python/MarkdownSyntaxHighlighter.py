import regex
from PySide2 import QtWidgets, QtGui

from MarkdownRegex import regexPatterns


class MarkdownSyntaxHighlighter(QtGui.QSyntaxHighlighter):
    """Syntax highlighter for markdown file"""

    IN_CODE_BLOCK = 1
    IN_METADATA_BLOCK = 2

    # Plaintext format options and regex
    text_formatter = QtGui.QTextCharFormat()
    text_formatter.setFontItalic(False)
    text_formatter.setFontWeight(QtGui.QFont.Normal)
    text_formatter.setFontStrikeOut(False)

    # Header format options and regex
    atx_header_pattern = regex.compile(regexPatterns['ATX_HEADER'], regex.MULTILINE)
    setext_header_pattern = regex.compile(regexPatterns['SETEXT_HEADER'], regex.MULTILINE)
    setext_underline_pattern = regex.compile(regexPatterns['SETEXT_UNDERLINE'], regex.MULTILINE)

    # Emphasis format options and regex
    emphasis_pattern = regex.compile(regexPatterns['EMPHASIS'], regex.MULTILINE)

    # Strong emphasis format options and regex
    strong_emphasis_pattern = regex.compile(regexPatterns['STRONG_EMPHASIS'], regex.MULTILINE)

    # Very strong emphasis options and regex
    very_strong_emphasis_pattern = regex.compile(regexPatterns['VERY_STRONG_EMPHASIS'], regex.MULTILINE)

    # Strikethrough emphasis options and regex
    strikethrough_pattern = regex.compile(regexPatterns['STRIKETHROUGH'], regex.MULTILINE)

    # Link options and regex
    link_pattern = regex.compile(regexPatterns['LINK'], regex.MULTILINE)
    angle_link_pattern = regex.compile(regexPatterns['ANGLE_LINK'], regex.MULTILINE)

    # Code block regex
    code_block_fence_pattern = regex.compile(regexPatterns['CODE_BLOCK_FENCE'], regex.MULTILINE)

    # Code inline regex
    code_inline_pattern = regex.compile(regexPatterns['CODE_INLINE'], regex.MULTILINE)

    # Metadata fence regex
    metadata_fence_pattern = regex.compile(regexPatterns['METADATA_FENCE'], regex.MULTILINE)

    def __init__(self, text_edit:QtWidgets.QTextEdit) -> None:
        """Initialise syntax highlighter.

        :param text_edit: QTextEdit to apply formatting to
        """
        super().__init__(text_edit)

    def highlightBlock(self, text:str) -> None:
        """Overrides QSyntaxHighlighter method to provide custom formatting"""

        formatter = QtGui.QTextCharFormat()

        self.setCurrentBlockState(0)

        # Setext header match and format
        for match in regex.finditer(self.setext_header_pattern, text + "\n" + self.currentBlock().next().text()):
            formatter.setFontWeight(QtGui.QFont.Bold)
            self.setFormat(match.start(), len(match.group()), formatter)

        # Setext underline match and format
        for match in regex.finditer(self.setext_underline_pattern, text):
            formatter.setFontWeight(QtGui.QFont.Bold)
            self.setFormat(match.start(), len(match.group()), formatter)

        # Atx header match and format
        for match in regex.finditer(self.atx_header_pattern, text):
            formatter.setFontWeight(QtGui.QFont.Bold)
            self.setFormat(match.start(), len(match.group()), formatter)


        # Emphasis match and format
        for match in regex.finditer(self.emphasis_pattern, text):
            formatter.setFontItalic(True)
            formatter.setFontWeight(QtGui.QFont.Normal)
            self.setFormat(match.start(), len(match.group()), formatter)

        # Strong emphasis match and format
        for match in regex.finditer(self.strong_emphasis_pattern, text):
            formatter.setFontWeight(QtGui.QFont.Bold)
            formatter.setFontItalic(False)
            self.setFormat(match.start(), len(match.group()), formatter)

        # Very strong emphasis match and format
        for match in regex.finditer(self.very_strong_emphasis_pattern, text):
            formatter.setFontItalic(True)
            formatter.setFontWeight(QtGui.QFont.Bold)
            self.setFormat(match.start(), len(match.group()), formatter)

        # Strikethrough match and format
        for match in regex.finditer(self.strikethrough_pattern, text):
            formatter.setFontStrikeOut(True)
            self.setFormat(match.start(), len(match.group()), formatter)

        # Link match and format
        for match in regex.finditer(self.link_pattern, text):
            formatter.setFontWeight(QtGui.QFont.Normal)
            formatter.setFontItalic(False)
            formatter.setFontStrikeOut(False)
            brush = QtGui.QBrush()
            brush.setColor(QtGui.QColor(125, 125, 125))
            brush.setStyle(QtGui.Qt.SolidPattern)
            formatter.setForeground(brush)
            self.setFormat(match.start("url"), len(match.group("url")), formatter)

        # Angle link match and format
        for match in regex.finditer(self.angle_link_pattern, text):
            formatter.setFontWeight(QtGui.QFont.Normal)
            formatter.setFontItalic(False)
            formatter.setFontStrikeOut(False)
            brush = QtGui.QBrush()
            brush.setColor(QtGui.QColor(125, 125, 125))
            brush.setStyle(QtGui.Qt.SolidPattern)
            formatter.setForeground(brush)
            self.setFormat(match.start("url"), len(match.group("url")), formatter)

        # Metadata block match and format
        metadata_start_index = 0
        # Change Formatter
        formatter.setFontWeight(QtGui.QFont.Normal)
        formatter.setFontItalic(False)
        formatter.setFontStrikeOut(False)
        brush = QtGui.QBrush()
        brush.setColor(QtGui.QColor(125, 125, 125))
        brush.setStyle(QtGui.Qt.SolidPattern)
        formatter.setForeground(brush)

        if self.previousBlockState() != self.IN_METADATA_BLOCK:
            try:
                if self.currentBlock().position() == 0:
                    metadata_start_index = regex.search(self.metadata_fence_pattern, text).start()
                else:
                    metadata_start_index = - 1
            except AttributeError:
                metadata_start_index = -1

        while metadata_start_index >= 0:
            match = regex.search(self.metadata_fence_pattern, text)
            metadata_end_index = match.start() if match is not None else None
            metadata_length = 0
            if metadata_end_index is None or self.previousBlockState() != self.IN_METADATA_BLOCK:
                self.setCurrentBlockState(self.IN_METADATA_BLOCK)
                metadata_length = len(text) - metadata_start_index
            else:
                metadata_length = metadata_end_index - metadata_start_index + len(match.group())
            self.setFormat(0, len(text), formatter)
            try:
                if self.previousBlockState() != self.IN_METADATA_BLOCK:
                    metadata_start_index = regex.search(self.metadata_fence_pattern, text[metadata_start_index + metadata_length:]).start()
                else:
                    metadata_start_index = -1
            except AttributeError:
                metadata_start_index = -1

        # Code block match and format
        start_index = 0
        # Change Formatter
        formatter.setFontWeight(QtGui.QFont.Normal)
        formatter.setFontItalic(False)
        formatter.setFontStrikeOut(False)
        brush = QtGui.QBrush()
        brush.setColor(QtGui.QColor(17, 168, 205 ))
        brush.setStyle(QtGui.Qt.SolidPattern)
        formatter.setForeground(brush)

        for match in regex.finditer(self.code_inline_pattern, text):
            self.setFormat(match.start(), len(match.group()), formatter)

        if self.previousBlockState() != self.IN_CODE_BLOCK:
            try:
                start_index = regex.search(self.code_block_fence_pattern, text).start()
            except AttributeError:
                start_index = -1

        while start_index >= 0:
            match = regex.search(self.code_block_fence_pattern, text)
            end_index = match.start() if match is not None else None
            comment_length = 0
            if end_index is None or self.previousBlockState() != self.IN_CODE_BLOCK:
                self.setCurrentBlockState(self.IN_CODE_BLOCK)
                comment_length = len(text) - start_index
            else:
                comment_length = end_index - start_index + len(match.group())

            self.setFormat(0, len(text), formatter)
            try:
                if self.previousBlockState() != self.IN_CODE_BLOCK:
                    start_index = regex.search(self.code_block_fence_pattern, text[start_index + comment_length: ]).start()
                else:
                    start_index = -1
            except AttributeError:
                start_index = -1




