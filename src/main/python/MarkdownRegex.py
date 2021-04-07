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
    'SETEXT_HEADER': r'(?:^\n*|\n\n)([^\s].+)\n {0,3}[=\-]+(?: +?\n|$)',
    'SETEXT_UNDERLINE': r'(=|-)+ *(?:\n+|$)'
}