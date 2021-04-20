regexPatterns = {
    'EMPHASIS':
        r'(?<!\\)\*[^\s\*](.*?\S?.*?)(?<!\\)\*'  # _word_
        r'|'
        r'(?<!(\\|\S))_[^\s_](.*?\S?.*?)(?<!\\)_(?=\s)'
     ,
    'STRONG_EMPHASIS':
        r'(\*\*|__)[^\s*](.*?\S.*?)\1'
     ,
    'VERY_STRONG_EMPHASIS':
     r'((\*\*|__)([*_])|([*_])(\*\*|__))[^\s*](.*?\S.*?)(?:\1)' # ***this*** or ___this___
     ,
    'STRIKETHROUGH': r'~~(?=\S)([\s\S]*?\S)~~', # ~~this~~
    'ATX_HEADER': r'^ *(#{1,6}) *([^\n]+?) *#* *(?:\n+|$)',
    'SETEXT_HEADER': r'(?:^\n*|\n\n)([^\s].+)\n{0,3}[=\-]+(?: +?\n|$)',
    'SETEXT_UNDERLINE': r'^(=|-)+ *(?:\n+|$)',
    'LINK': r'\[(?P<text>.*)\]\((?P<url>.+?)(?: \"(?P<title>.+)\")?\)',
    'ANGLE_LINK': r"<(?P<text>(?P<url>[A-Za-z][A-Za-z0-9.+-]{1,31}:[^<>\x00-\x20]*|(?:[a-zA-Z0-9.!#$%&'*+\/=?^_`{|}~-]+@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*)))>",
    'CODE_BLOCK_FENCE': r'(?:^|\n) {0,3}([`~]{3})',
    'CODE_INLINE': r'`[^`\n\r]+`'
}