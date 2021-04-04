regexPatterns = [
    ('EMPHASIS',
     r'(?<!\\)\*[^\s\*](.*?\S?.*?)(?<!\\)\*|(?<!(\\|\S))_[^\s_](.*?\S?.*?)(?<!\\)_(?=\s)' # *this*
     ),
    ('STRONG_EMPHASIS',
     r'(\*\*|__)[^\s*](.*?\S.*?)(\*\*|__)' # **this** or __this__
     ),
    ('VERY_STRONG_EMPHASIS',
     r'((\*\*|__)([*_])|([*_])(\*\*|__))[^\s*](.*?\S.*?)((\*\*|__)([*_])|([*_])(\*\*|__))' # ***this*** or ___this___
     ),
    ('STRIKETHROUGH', r'~~(?=\S)([\s\S]*?\S)~~'), # ~~this~~
    ('HEADER', r'^ *(#{1,6}) *([^\n]+?) *#* *(?:\n+|$)|^([^\n]+)\n *(=|-)+ *(?:\n+|$)'),
    ('TEXT', r'.')
]