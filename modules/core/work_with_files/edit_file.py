"""
Это модуль для работы с файлами
"""

import os
import enum
import io

from typing import assert_never, NoReturn

from pygments.lexer import LexerMeta
from kivy.factory import Factory

from modules.core.get_settings.get_settings import Settings


class DataOfFilesTypes:
    """
    Данные о типах файлов:
        FileType - поддерживаемые типы файлов
        types - типы файлов по расширению
        get_type_by_path - получение типа по пути
        get_lexer_by_type - получение lexer'а по типу
    """

    class FileType(enum.Enum):
        """
        Variables:
            PY – Python,
            JS – JavaScript,
            JSON – JSON,
            MD – Markdown,
            HTML – HTML,
            CSS – CSS,
            C – C,
            CPP – C++,
            JAVA – Java,
            SH – Shell/Bash,
            KV – KvLang,
            TXT – Other.
        """

        PY = "py"
        JS = "js"
        JSON = "json"
        MD = "md"
        HTML = "html"
        CSS = "css"
        C = "c"
        CPP = "cpp"
        JAVA = "java"
        SH = "sh"
        KV = "kv"
        TXT = "txt"

    @staticmethod
    def get_type_by_path(path: str) -> FileType:
        extension: str = path.split(".")[-1] if len(path.split(".")) > 1 else "txt"
        if extension in DataOfFilesTypes.FileType._value2member_map_.keys():
            return DataOfFilesTypes.FileType._value2member_map_[extension]  # type: ignore
        return DataOfFilesTypes.FileType.TXT

    @staticmethod
    def get_lexer_by_type(type_file: FileType) -> LexerMeta:
        """
        Args:
            type_file (FileType): Элемент перечисления FileType

        Returns:
            LexerMeta: Не объект, а класс
        """
        match type_file:
            case DataOfFilesTypes.FileType.PY:
                from pygments.lexers.python import PythonLexer

                return PythonLexer
            case DataOfFilesTypes.FileType.C:
                from pygments.lexers.c_cpp import CLexer

                return CLexer
            case DataOfFilesTypes.FileType.CPP:
                from pygments.lexers.c_cpp import CppLexer

                return CppLexer
            case DataOfFilesTypes.FileType.JS:
                from pygments.lexers.javascript import JavascriptLexer

                return JavascriptLexer
            case DataOfFilesTypes.FileType.HTML:
                from pygments.lexers.html import HtmlLexer

                return HtmlLexer
            case DataOfFilesTypes.FileType.CSS:
                from pygments.lexers.css import CssLexer

                return CssLexer
            case DataOfFilesTypes.FileType.MD:
                from pygments.lexers.markup import MarkdownLexer

                return MarkdownLexer
            case DataOfFilesTypes.FileType.JSON:
                from pygments.lexers.markup import JsonLexer

                return JsonLexer
            case DataOfFilesTypes.FileType.JAVA:
                from pygments.lexers.jvm import JavaLexer

                return JavaLexer
            case DataOfFilesTypes.FileType.SH:
                from pygments.lexers.shell import BashLexer

                return BashLexer
            case DataOfFilesTypes.FileType.TXT:
                from pygments.lexers.special import TextLexer

                return TextLexer
            case DataOfFilesTypes.FileType.KV:
                from kivy.extras.highlight import KivyLexer

                return KivyLexer
            case _ as unreachable:
                assert_never(unreachable)


class EditFile:
    """Класс для работы с файлами"""

    _file: io.TextIOWrapper
    _type: DataOfFilesTypes.FileType
    _path: str
    lexer: LexerMeta
    text: str

    def __init__(self, path: str = "") -> None:
        self._path = ""
        self._type = DataOfFilesTypes.FileType.TXT
        self.set_lexer()
        self.text = ""
        if path != "":
            self.open(path)

    def open(self, path: str = "") -> None | NoReturn:
        """Открывает файл, если файла нет создаёт его"""

        self.text = ""
        try:
            self._path = os.path.abspath(path)
            self.text = open(path, "r", encoding="utf-8").read()
        except FileNotFoundError:
            try:
                os.makedirs(os.path.dirname(self._path), exist_ok=True)
                open(self._path, "w", encoding="utf-8").close()
            except Exception as err:
                raise err
        except PermissionError:
            raise Exception("Нет прав на чтение")
        except Exception:
            raise Exception("Путь некорректен")

        self.set_type()
        self.set_lexer()

    def save(self) -> None | NoReturn:
        if self._path == "":
            raise Exception("Путь не указан")
        try:
            os.makedirs(os.path.dirname(self._path), exist_ok=True)
            with open(self._path, "w", encoding="utf-8") as self._file:
                self._file.write(self.text)
        except PermissionError:
            raise Exception("Нет прав на запись")
        except Exception:
            raise Exception("Путь некорректен")

    def save_as(self, target_path: str) -> None | NoReturn: ...

    # TODO: run-метод для разных ОС
    def run(self) -> None | NoReturn:
        match self._type:
            case DataOfFilesTypes.FileType.PY:
                try:
                    exec(self.text)
                except Exception as err:
                    raise err
            case _:
                ...
        ...

    def delete(self) -> None | NoReturn:
        try:
            os.remove(self._path)
        except PermissionError:
            raise Exception("Нет прав на удаление")
        except Exception:
            raise Exception("Путь некорректен")

    def get_path(self) -> str:
        return self._path

    def get_type(self) -> DataOfFilesTypes.FileType:
        return self._type

    def set_type(self) -> None:
        self._type = DataOfFilesTypes.get_type_by_path(self._path)

    def set_lexer(self) -> None:
        self.lexer = DataOfFilesTypes.get_lexer_by_type(self._type)()

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(path={self._path}, type={self._type}, lexer={self.lexer}, text='{self.text}')"


class EditFileForApp(EditFile):
    readonly: bool

    @staticmethod
    def get_abs_path(path: str) -> str:
        if path[0] == "$" and Settings():
            path = path[1:]
            if len(path.split("/")) == 1:  # Это файл
                if path in Settings().get("RESERVED_PATHS", []):
                    path = Settings()["RESERVED_PATHS"][path]["path"]
                elif path in Settings().get("user_aliases", []):
                    path = Settings()["user_aliases"][path]
                else:
                    Factory.PushMessage(
                        f"Переменная {path} не найдена",
                        type_message="error",
                    ).show_message()
                    path = Settings()["RESERVED_PATHS"]["welcome"]["path"]
            elif len(path.split("/")) > 1:  # Это директория
                var_dir: str = path.split("/")[0]
                if var_dir in Settings().get("RESERVED_PATHS", []):
                    path = Settings()["RESERVED_PATHS"][var_dir]["path"] + "".join(
                        "/" + p for p in path[1:].split("/")[1:]
                    )
                elif var_dir in Settings().get("user_aliases", []):
                    path = Settings()["user_aliases"][var_dir] + "".join(
                        "/" + p for p in path[1:].split("/")[1:]
                    )
                else:
                    Factory.PushMessage(
                        f"Переменная {path} не найдена",
                        type_message="error",
                    ).show_message()
                    path = Settings()["RESERVED_PATHS"]["welcome"]["path"]

            path = EditFileForApp.get_abs_path(path)

        return os.path.abspath(path)

    @staticmethod
    def get_readonly(path: str) -> bool:
        if not Settings():
            return False
        path = EditFileForApp.get_abs_path(path)
        for key in Settings().get("RESERVED_PATHS", []):
            if (
                EditFileForApp.get_abs_path(Settings()["RESERVED_PATHS"][key]["path"])
                == path
            ):
                return Settings()["RESERVED_PATHS"][key]["readonly"]
        return False

    def open(self, path: str = "$welcome") -> None:
        if path == "":
            path = "$welcome"
        path = EditFileForApp.get_abs_path(path)
        self.readonly = EditFileForApp.get_readonly(path)
        try:
            super().open(path)
        except Exception as err:
            Factory.PushMessage(
                f"Файл не может быть открыт/создан:\n{err}",
                type_message="error",
            ).show_message()

    def save(self) -> None:
        if self.readonly:
            Factory.PushMessage(
                "Файл доступен только для чтения",
                type_message="warning",
            ).show_message()
            return
        try:
            super().save()
        except Exception as err:
            Factory.PushMessage(
                f"Файл не может быть сохранён:\n{err}",
                type_message="error",
            ).show_message()

    def delete(self) -> None:
        if self.readonly:
            Factory.PushMessage(
                "Файл доступен только для чтения",
                type_message="warning",
            ).show_message()
            return
        if self._path == EditFileForApp.get_abs_path("$settings"):
            Factory.PushMessage(
                "Файл не может быть удалён", type_message="warning"
            ).show_message()
            return
        try:
            super().delete()
        except Exception as err:
            Factory.PushMessage(
                f"Файл не может быть удалён:\n{err}",
                type_message="error",
            ).show_message()

    def run(self) -> None:
        if self.readonly:
            Factory.PushMessage(
                "Файл доступен только для чтения",
                type_message="warning",
            ).show_message()
            return
        elif self._type != DataOfFilesTypes.FileType.PY:
            Factory.PushMessage(
                "Приложение пока не поддерживает запуск этого типа файлов\n"
                + "Но вы можете попробовать запустить Python код",
                type_message="warning",
            ).show_message()
            return

        try:
            super().run()
        except Exception as err:
            Factory.PushMessage(
                f"Что-то пошло не так:\n{err}",
                type_message="error",
            ).show_message()
