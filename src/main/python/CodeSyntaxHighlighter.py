import mistune
from pygments import highlight
from pygments.formatters import html
from pygments.lexers import get_lexer_by_name


class HighlightRenderer(mistune.Renderer):
    def block_code(self, code, lang=None):
        if lang:
            try:
                lexer = get_lexer_by_name(lang, stripall=True)
                formatter = html.HtmlFormatter(style='emacs', noclasses=True)
                return highlight(code, lexer, formatter)
            except ValueError:
                pass
        return '<pre><code>' + mistune.escape(code) + '</code></pre>'

    def strikethrough(self, text):
        """Rendering ~~strikethrough~~ text. Overrides standard method which uses <del> and is unsupported by qt

        :param text: text content for strikethrough.
        """
        return '<s>%s</s>' % text


