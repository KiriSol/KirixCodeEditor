from typing import Any

from modules.uix.code_input_widget.code_input_line_number import CodeInputLineNumber
from modules.core.work_with_files.edit_file import EditFileForApp


class CodeInputToFile(CodeInputLineNumber):
    file: EditFileForApp

    def __init__(self, **kwargs: dict[str, Any]) -> None:
        super().__init__(**kwargs)
        self.file = EditFileForApp()

    def open(self, path: str = "$welcome") -> None:
        self.file.open(path)

        self.text = self.file.text
        self.lexer = self.file.lexer
        # self.text_content.readonly = self.file.readonly
        self.set_cursor_line(1)

    def save(self) -> None:
        self.file.text = self.text
        self.file.save()

    def save_as(self, path: str) -> None:
        self.file.text = self.text
        self.file.save_as(path)

    def run(self) -> None:
        self.file.text = self.text
        self.file.run()

    def delete(self) -> None:
        self.file.delete()
        self.open()

    def get_path(self) -> str:
        return self.file.get_path()
