regexPatterns = {
    'EMPHASIS':
        r'^\b_((?:__|[^_])+?)_\b'  # _word_
        r'|'
        r'^\*((?:\*\*|[^\*])+?)\*(?!\*)'
     ,
    'STRONG_EMPHASIS':
        r'^_{2}([\s\S]+?)_{2}(?!_)'  # __word__
        r'|'
        r'^\*{2}([\s\S]+?)\*{2}(?!\*)'  # **word**
     ,
    'VERY_STRONG_EMPHASIS':
     r'((\*\*|__)([*_])|([*_])(\*\*|__))[^\s*](.*?\S.*?)((\*\*|__)([*_])|([*_])(\*\*|__))' # ***this*** or ___this___
     ,
    'STRIKETHROUGH': r'~~(?=\S)([\s\S]*?\S)~~', # ~~this~~
    'ATX_HEADER': r'^ *(#{1,6}) *([^\n]+?) *#* *(?:\n+|$)',
    'SETEXT_HEADER': r'(?:^\n*|\n\n)([^\s].+)\n {0,3}[=\-]+(?: +?\n|$)',
    'SETEXT_UNDERLINE': r'(=|-)+ *(?:\n+|$)'
}