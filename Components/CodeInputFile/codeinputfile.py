# My Modules
from Components.EditFile.editfile import EditFile
from Components.TextLine.textinputlinenumber import CodeInputLineNumber

# Kivy
from kivy.properties import (
    ObjectProperty,
    StringProperty
)


class CodeInputFile(CodeInputLineNumber):
    file = EditFile()
    text = StringProperty("")
    
    def open_file(self, path: str = None) -> None:
        self.file.open_file(path)
        self.text = self.file.text
        self.set_lexer()
        print(self.lexer)
    
    def save_file(self) -> None:
        self.file.text = self.text
        self.file.save_file()
    
    def run_file(self):
        self.file.run_file()
    
    def set_lexer(self) -> None:
        self.file.set_lexer()
        self.text_content.lexer = self.file.lexer
    
    def which_file(self) -> None | str:
        return self.file.get_path()
    
    def __repr__(self) -> str:
        return f"CodeInputFile(file={self.file})"