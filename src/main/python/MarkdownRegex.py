import regex
regexPatterns = [
    ('HEADER', r'^ *(#{1,6}) *([^\n]+?) *#* *(?:\n+|$)|^([^\n]+)\n *(=|-)+ *(?:\n+|$)', regex.MULTILINE),
    ('EMPHASIS',
        r'(?<!\\)\*[^\s\*](.*?\S?.*?)(?<!\\)\*|(?<!(\\|\S))_[^\s_](.*?\S?.*?)(?<!\\)_(?=\s)' # *this*
    ),
    ('STRONG_EMPHASIS',
        r'(\*\*|__)[^\s*](.*?\S.*?)\1' # **this** or __this__
    ),
    ('VERY_STRONG_EMPHASIS',
        r'((\*\*|__)([*_])|([*_])(\*\*|__))[^\s*](.*?\S.*?)(?:\5\4|\3\2)' # ***this*** or ___this___
    ),
    ('STRIKETHROUGH', r'~~(?=\S)([\s\S]*?\S)~~'), # ~~this~~
    ('TEXT', r'[\s\S]+?(?=[\\<!\[_*`~]|https?://| {2,}\n|$)')
]