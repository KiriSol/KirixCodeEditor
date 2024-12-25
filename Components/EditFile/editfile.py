"""
Это модуль для работы с файи
"""

import os
import io

def create_directory(dir_path: str):
    try:
        os.makedirs(dir_path, exist_ok=True)
        return 0
    except OSError:
        return 1


class EditFile:
    _path: str = None
    _type: str = None
    _file: io.TextIOWrapper = None
    lexer = None
    text: str = ""

    def open_file(self, path: str = "") -> None:
        self.text = ""

        if path == "" or path is None:  # Проверяем наличие пути
            raise NameError("Путь не указан")
        
        try:  # Пытаемся получить абсолютный путь
            self._path = os.path.abspath(path)
            self._type = self._path.split(".")[-1]
            self.set_lexer()
        except:
            raise NameError("Путь некорректен")

        try:  # Пытаемся открыть файл
            with open(self._path, "r", encoding="utf-8") as file:
                self.text = file.read()
        except FileNotFoundError as err:  # Если файл не найден, пытаемся создать
            try:
                create_directory(os.path.dirname(self._path))  # Создаем директорию
                open(self._path, "w", encoding="utf-8").close()  # Создаем пустой файл
            except:
                raise NameError("Путь некорректен")

    def save_file(self) -> None:
        if self._path is None:  # Проверяем наличие пути
            # raise NameError("Path is invalid (None)")
            return
        elif self._path == "":
            return

        try:  # Пытаемся сохранить
            with open(self._path, "w", encoding="utf-8") as file:
                file.write(self.text)
        except FileNotFoundError as err:  # Если файл не найден, пытаемся создать

            if "directory" in err.strerror:
                if create_directory(os.path.dirname(self._path)):  # Создаем директорию
                    self._path = "./" + self._path
                with open(self._path, "w", encoding="utf-8") as file:  # Создаем файл
                    file.write(self.text)

            else:  # Если не удалось создать файл
                raise NameError("Path is invalid (None)")

    def run_file(self) -> None:
        if self._path == "":  # Проверяем наличие пути
            return
        
        if self._type == "py":
            os.system(f"python {self._path}")
        elif self._type == "c":
            os.system(f"gcc {self._path} -o {self._path.split('.')[0]}")
            os.system(f"./{self._path.split('.')[0]}")
        elif self._type == "cpp":
            os.system(f"g++ {self._path} -o {self._path.split('.')[0]}")
            os.system(f"{self._path.split('.')[0]}")
        elif self._type == "js":
            os.system(f"node {self._path}")
        elif self._type == "html":
            os.system(f"start {self._path}")
        else:
            self.save_file()

    def set_lexer(self) -> None:
        if self._type == "py":
            from pygments.lexers.python import PythonLexer

            self.lexer = PythonLexer()
        elif self._type == "c":
            from pygments.lexers.c_cpp import CLexer

            self.lexer = CLexer()
        elif self._type == "cpp":
            from pygments.lexers.c_cpp import CppLexer

            self.lexer = CppLexer()
        elif self._type == "js":
            from pygments.lexers.javascript import JavascriptLexer

            self.lexer = JavascriptLexer()
        elif self._type == "html":
            from pygments.lexers.html import HtmlLexer

            self.lexer = HtmlLexer()
        elif self._type == "css":
            from pygments.lexers.css import CssLexer

            self.lexer = CssLexer()
        elif self._type == "json":
            from pygments.lexers.jsonnet import JsonnetLexer

            self.lexer = JsonnetLexer()
        elif self._type == "md":
            from pygments.lexers.markup import MarkdownLexer

            self.lexer = MarkdownLexer()
        elif self._type == "kv":
            from kivy.extras.highlight import KivyLexer

            self.lexer = KivyLexer()
        else:
            from pygments.lexers.text import IniLexer

            self.lexer = IniLexer()

    def get_path(self) -> None | str:
        return self._path

    def __repr__(self) -> str:
        return f"EditFile(path={self._path}, lexer={self._lexer})"

    def __str__(self) -> str:
        return f'<{type(self).__name__}> "{self._path}"'
