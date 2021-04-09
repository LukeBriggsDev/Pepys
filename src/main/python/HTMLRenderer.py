import mistune
from pygments import highlight
from pygments.formatters import html
from pygments.lexers import get_lexer_by_name
from mistune import escape


class HighlightRenderer(mistune.Renderer):
    """Custom renderer for markdown to html conversion"""

    def block_code(self, code: str, lang: str = None) -> str:
        """ Render markdown code blocks as html.

        :param code: the text within the code block
        :param lang: the specified programming language (default = None)
        :return: highlighted code if language recognised, else plain monospaced text
        """
        if lang:
            try:
                lexer = get_lexer_by_name(lang, stripall=True)
                formatter = html.HtmlFormatter(style='emacs', noclasses=True, nobackground=True)
                return highlight(code, lexer, formatter)
            except ValueError:
                pass
        return '<pre><code>' + mistune.escape(code) + '</code></pre>'

    def codespan(self, text):
        """Rendering inline `code` text.

        :param text: text content for inline code.
        """
        text = escape(text.rstrip(), smart_amp=False)
        return '<code style="background-color: rgba(0, 0, 0, 0.11);">%s</code>' % text

    def strikethrough(self, text: str) -> str:
        """Rendering ~~strikethrough~~ text. Overrides standard method which uses <del> and is unsupported by qt

        :param text: text content for strikethrough.
        """
        return '<s>%s</s>' % text


