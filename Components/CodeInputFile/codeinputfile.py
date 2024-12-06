from Components.EditFile.editfile import EditFile
from Components.TextLine.textinputlinenumber import TextInputLineNumber

from kivy.properties import (
    ObjectProperty,
    StringProperty
)


class CodeInputFile:
    def __init__(self, path, lexer):
        self.code_input = ObjectProperty(None)
        
        self.edit_file = EditFile(path, lexer)
    
    def __repr__(self):
        return f"CodeInFile(path={self.edit_file.path}, lexer={self.edit_file.lexer})"
    
    def open_file(self, path: str = None):
        self.edit_file.open_file(path)
        