import regex
from PyQt5 import QtWidgets, QtGui, QtCore
import CONSTANTS
from MarkdownRegex import regexPatterns
import enchant
from enchant.tokenize import get_tokenizer
from enchant.tokenize import EmailFilter, URLFilter
from CONSTANTS import spell_dict, spell_lang
import CONSTANTS
from ColorParser import text_to_rgb

class MarkdownSyntaxHighlighter(QtGui.QSyntaxHighlighter):
    """Syntax highlighter for markdown file"""

    IN_CODE_BLOCK = 1
    IN_METADATA_BLOCK = 2
    # Load tokenizer
    try:
        spell_tknzr = get_tokenizer(spell_lang, filters=[EmailFilter, URLFilter])
    except enchant.errors.TokenizerNotFoundError:
        spell_tknzr = get_tokenizer(filters=[EmailFilter, URLFilter])

    # Header format options and regex
    atx_header_pattern = regex.compile(regexPatterns['ATX_HEADER'], regex.MULTILINE)
    setext_header_pattern = regex.compile(regexPatterns['SETEXT_HEADER'], regex.MULTILINE)
    setext_underline_pattern = regex.compile(regexPatterns['SETEXT_UNDERLINE'], regex.MULTILINE)

    # Separator regex
    separator_pattern = regex.compile(regexPatterns['SEPARATOR'], regex.MULTILINE)

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

        # Spell Checking
        # A word is underlined red
        misspelled = [token[0] for token in self.spell_tknzr(text)
                      if token[0][0].islower() and # doesn't start with a capital letter
                      not spell_dict.check(token[0])] # isn't in the dictionary
        for word in misspelled:
            for match in regex.finditer(r"\b" + regex.escape(word) + r"(?=\W)", text):
                formatter.setUnderlineColor(QtGui.QColor(200, 0, 0))
                formatter.setUnderlineStyle(QtGui.QTextCharFormat.SpellCheckUnderline)
                formatter.setFontUnderline(True)
                self.setFormat(match.start(), len(match.group()), formatter)
                formatter.setFontUnderline(False)

                self.setFormat(match.end(), 1, formatter)

        # Setext header match and format. Only if there is a newline before hand
        if (self.currentBlock().previous().text() == "" ):
                for match in regex.finditer(self.setext_header_pattern, text + "\n" + self.currentBlock().next().text()):
                    formatter.setFontWeight(QtGui.QFont.Bold)
                    self.setFormat(match.start(), len(match.group()), formatter)

        # Setext underline match and format
        for match in regex.finditer(self.setext_underline_pattern, text):
            formatter.setFontWeight(QtGui.QFont.Bold)
            self.setFormat(match.start(), len(match.group()), formatter)

        # Atx header match and format. Only if there is a newline or separator beforehand,
        if (self.currentBlock().previous().text() == "" or
                regex.search(self.separator_pattern, self.currentBlock().previous().text())) \
                and not regex.search(self.setext_underline_pattern, self.currentBlock().next().text()):

            for match in regex.finditer(self.atx_header_pattern, text):
                formatter.setFontWeight(QtGui.QFont.Bold)
                self.setFormat(match.start(), len(match.group()), formatter)
                # Grey out hashes
                brush = QtGui.QBrush()
                color = CONSTANTS.colors
                brush.setColor(text_to_rgb(CONSTANTS.colors[CONSTANTS.theme]["lowlight"]))
                brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
                formatter.setForeground(brush)
                self.setFormat(match.start(), len(match.group('level')), formatter)


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
            brush.setColor(text_to_rgb(CONSTANTS.colors[CONSTANTS.theme]["lowlight"]))
            brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
            formatter.setForeground(brush)
            formatter.setFontUnderline(QtGui.QTextCharFormat.NoUnderline)
            self.setFormat(match.start("url"), len(match.group("url")), formatter)

        # Angle link match and format
        for match in regex.finditer(self.angle_link_pattern, text):
            formatter.setFontWeight(QtGui.QFont.Normal)
            formatter.setFontItalic(False)
            formatter.setFontStrikeOut(False)
            brush = QtGui.QBrush()
            brush.setColor(text_to_rgb(CONSTANTS.colors[CONSTANTS.theme]["lowlight"]))
            brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
            formatter.setForeground(brush)
            formatter.setFontUnderline(QtGui.QTextCharFormat.NoUnderline)
            self.setFormat(match.start("url"), len(match.group("url")), formatter)

        # Metadata block match and format
        metadata_start_index = 0
        # Change Formatter
        formatter.setFontWeight(QtGui.QFont.Normal)
        formatter.setFontItalic(False)
        formatter.setFontStrikeOut(False)
        brush = QtGui.QBrush()
        brush.setColor(text_to_rgb(CONSTANTS.colors[CONSTANTS.theme]["text_alt"]))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        formatter.setForeground(brush)

        self.format_fence(text, self.metadata_fence_pattern, formatter, self.IN_METADATA_BLOCK, required_start_block_positon=0)

        # Inline code block match and format
        for match in regex.finditer(self.code_inline_pattern, text):
            inline_formatter = QtGui.QTextCharFormat()
            inline_formatter.setFontWeight(QtGui.QFont.Normal)
            inline_formatter.setFontItalic(False)
            inline_formatter.setFontStrikeOut(False)
            brush = QtGui.QBrush()
            brush.setColor(text_to_rgb(CONSTANTS.colors[CONSTANTS.theme]["inline_code_bg"]))
            brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
            inline_formatter.setBackground(brush)
            inline_formatter.setUnderlineStyle(QtGui.QTextCharFormat.NoUnderline)
            self.setFormat(match.start(), len(match.group()), inline_formatter)

        # Code block match and format
        # Change Formatter
        formatter = QtGui.QTextCharFormat()
        formatter.setFontWeight(QtGui.QFont.Normal)
        formatter.setFontItalic(False)
        formatter.setFontStrikeOut(False)
        brush = QtGui.QBrush()
        brush.setColor(text_to_rgb(CONSTANTS.colors[CONSTANTS.theme]["code_block_text"]))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        formatter.setForeground(brush)
        formatter.setFontUnderline(QtGui.QTextCharFormat.NoUnderline)

        self.format_fence(text, self.code_block_fence_pattern, formatter, self.IN_CODE_BLOCK)




    def format_fence(self, text: str, fence_pattern, formatter: QtGui.QTextCharFormat, block_state_flag: int,
                     required_start_block_positon:int = None):
        """Used to format blocks that are fenced
        :param text: the text of the current block
        :param fence_pattern: the regex pattern matching the fence
        :param formatter: the QTextCharFormat to apply to the block
        :param block_state_flag: the flag to use to check against block state
        """
        start_index = 0
        if self.previousBlockState() != block_state_flag:
            try:
                if required_start_block_positon is None:
                    start_index = regex.search(fence_pattern, text).start()
                elif self.currentBlock().position() == required_start_block_positon:
                    start_index = regex.search(fence_pattern, text).start()
                else:
                    start_index = -1
            except AttributeError:
                start_index = -1

        while start_index >= 0:
            matches = [match for match in regex.finditer(fence_pattern, text)][0::2]
            end_index = matches[0].start() if matches != [] else None
            block_length = 0
            if end_index is None or self.previousBlockState() != block_state_flag:
                self.setCurrentBlockState(block_state_flag)
                block_length = len(text) - start_index
            else:
                block_length = end_index - start_index + len(matches[0].group())

            self.setFormat(start_index, block_length, formatter)
            try:
                if self.previousBlockState() != block_state_flag:
                    start_index = regex.search(fence_pattern, text[start_index + block_length: ]).start()
                else:
                    start_index = -1
            except AttributeError:
                start_index = -1

