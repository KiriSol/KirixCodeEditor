from io import TextIOWrapper
import os
import json

from pygments.lexers.c_cpp import CppLexer

from kivy.app import App
from kivy.properties import ObjectProperty, StringProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.lang.builder import Builder

from TextLine.textinputlinenumber import TextInputLineNumber

settings= json.load(open("./.config/settings.json", "r"))
print(settings)


Builder.load_file("./kv/codeeditor.kv")
Builder.load_file("./kv/textinputlinenumber.kv")

os.makedirs("./.config", exist_ok=True)

settings = json.load(open("./.config/settings.json", "r"))
file_path = settings["path_file"]


class EditFile:
    def __init__(self, path):
        
        self.path = path
        self.file: TextIOWrapper

        self.open_file(path)

    def open_file(cls, path):
        pass
    # TODO: methods

1
class CodeEditorRoot(BoxLayout):
    lni = ObjectProperty(None)
    text = StringProperty("")

    def delete(self, instance=None):
        self.lni.text = ""
        self.lni.text_content.focus = True

    def save(self, instance=None):
        with open(file_path, "w") as file:
            file.write(self.lni.text)

    def tab(self, instance=None):
        self.lni.text_content.insert_text("\t")
        self.lni.text_content.focus = True

    def open_file(self, path_file):
        global file_path; file_path = path_file
        with open(file_path, "r") as file, open("path.txt", "w") as path:
            self.lni.text_content.text = file.read()
            path.write(file_path)
        print(file_path)

    def run(self, instance=None):
        self.save()
        # os.system(f'g++ {file_path} -o {file_path.replace(".cpp", '')}')
        # os.system(file_path.replace(".cpp", ''))
        run_path = file_path.replace(("." + file_path.split(".")[-1]), "")
        os.system(f"g++ {file_path} -o {run_path}")
        os.system('start cmd /k ' + run_path)
        # print(f"g++ {file_path} -o {run_path}")
        # print(f"{run_path}")


class CodeEditorApp(App):

    def build(self):
        res = BoxLayout()

        # res.add_widget(BoxLayout(orientation="vertical", size_hint=(0.1, 1)))
        root = CodeEditorRoot()
        root.lni.text_content.lexer = CppLexer()
        root.path_file.text = file_path
        try:
            with open(file_path, "r") as file:
                root.lni.text = file.read()
        except FileNotFoundError:
            with open(file_path, "w") as file:
                file.write('''
#include <iostream>

int main() {
    std::cout << "Hello, World!" << std::endl;
    return 0;
}''')

        with open(file_path, "r") as file:
            root.lni.text = file.read()
        res.add_widget(root)
        return res


if __name__ == "__main__":
    CodeEditorApp().run()
