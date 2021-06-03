"""
    Some of this regex was derived from the Apostrophe project
    <https://gitlab.gnome.org/World/apostrophe/-/blob/e6897178648d40e0617babc5bd9e2fce14060de5/apostrophe/markup_regex.py>

    Copyright (C) 2021  Manuel Genovés
                  2021  Luke Briggs <lukebriggs02@gmail.com>

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""
regexPatterns = {
    'EMPHASIS':
        r'(?<!\\)\*[^\s\*](.*?\S?.*?)(?<!\\)\*'  # *word*
        r'|'
        r'(?<!(\\|\S))_[^\s_](.*?\S?.*?)(?<!\\)_(?=(\s|$))' # _word_
     ,
    'STRONG_EMPHASIS':
        r'(\*\*|__)[^\s*](.*?\S.*?)\1'
     ,
    'VERY_STRONG_EMPHASIS':
     r'((\*\*|__)([*_])|([*_])(\*\*|__))[^\s*](.*?\S.*?)(?:\1)' # ***this*** or ___this___
     ,
    'STRIKETHROUGH': r'~~(?=\S)([\s\S]*?\S)~~', # ~~this~~
    'ATX_HEADER': r'^ *(?P<level>#{1,6}) +([^\n]+?) *#* *(?:\n+|$)',
    'SETEXT_HEADER': r'(?:^\n*|\n\n)([^\s].+)\n[=\-]+(?: +?\n|$)',
    'SETEXT_UNDERLINE': r'^(=|-)+ *(?:\n+|$)',
    'SEPARATOR': r'^(-)+ *(?:\n+|$)',
    'LINK': r'\[(?P<text>.*?)\]\((?P<url>.+?)(?: \"(?P<title>.+)\")?\)',
    'ANGLE_LINK': r"<(?P<text>(?P<url>[A-Za-z][A-Za-z0-9.+-]{1,31}:[^<>\x00-\x20]*|(?:[a-zA-Z0-9.!#$%&'*+\/=?^_`{|}~-]+@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*)))>",
    'HTML_TAG': r"<.*>",
    'CODE_BLOCK_FENCE': r'(?:^|\n) {0,3}([`~]{3})',
    'CODE_INLINE': r'(`{1,2}.*?`{1,2})',
    'METADATA_FENCE': r'(?:^|\n)([-]{3})(?!.)',
}