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