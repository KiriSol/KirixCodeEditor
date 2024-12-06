'''


'''


class EditFile:
    def __init__(self, path: str = "__welcome__", lexer: object = None):
        self.path = path
        self.type = path.split(".")[-1]
        if lexer is None:
            self.set_lexer()
        else:
            self.lexer = lexer

        self.file = None

    def open_file(self, path: str = None):
        if path is None:
            pass
        else:
            self.__init__(path)

        try:
            self.file = open(self.path, "r", encoding="utf-8")
        except FileNotFoundError as err:
            open(self.path, "w", encoding="utf-8").close()
            self.file = open(self.path, "r", encoding="utf-8")

        self.text = self.file.read()
        self.file.close()

    def save_file(self):
        with open(self.path, "w", encoding="utf-8") as file:
            file.write(self.text)

    def set_lexer(self):
        if self.type == "py":
            from pygments.lexers.python import PythonLexer

            self.lexer = PythonLexer()
        elif self.type == "c":
            from pygments.lexers.c_cpp import CLexer

            self.lexer = CLexer()
        elif self.type == "cpp":
            from pygments.lexers.c_cpp import CppLexer

            self.lexer = CppLexer()
        elif self.type == "js":
            from pygments.lexers.javascript import JavascriptLexer

            self.lexer = JavascriptLexer()
        elif self.type == "html":
            from pygments.lexers.html import HtmlLexer

            self.lexer = HtmlLexer()
        elif self.type == "css":
            from pygments.lexers.css import CssLexer

            self.lexer = CssLexer()
        elif self.type == "json":
            from pygments.lexers.javascript import JsonLexer

            self.lexer = JsonLexer()
        elif self.type == "txt":
            from pygments.lexers.text import TextLexer

            self.lexer = TextLexer()
        elif self.type == "md":
            from pygments.lexers.markup import MarkdownLexer

            self.lexer = MarkdownLexer()
        elif self.type == "kv":
            from kivy.extras.highlight import KivyLexer

            self.lexer = KivyLexer()
        else:
            self.lexer = None

    def get_lexer(self):
        return self.lexer

    def get_path(self):
        return self.path

    def __repr__(self):
        return f"EditFile(path={self.path}, lexer={self.lexer})"

    def __str__(self):
        return f'<{type(self).__name__}> "{self.path}"'
