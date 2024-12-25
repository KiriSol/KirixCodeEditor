from io import TextIOWrapper
import os
import json

# Kivy
from kivy.app import App
from kivy.properties import ObjectProperty, StringProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.lang.builder import Builder

# My Modules
from Components.TextLine.textinputlinenumber import CodeInputLineNumber
from Components.EditFile.editfile import EditFile
from Components.CodeInputFile.codeinputfile import CodeInputFile

# KV
Builder.load_file("./kv/textinputlinenumber.kv")
Builder.load_file("./kv/codeinputfile.kv")

Builder.load_file("./kv/main.kv")

# os.makedirs("./.kirix", exist_ok=True)

# Open Settings
settings = json.load(open("./.kirix/settings.json", "r"))


class CodeEditorRoot(BoxLayout):
    work_code = ObjectProperty(None)


class KirixApp(App):
    def build(self):
        return CodeEditorRoot()


if __name__ == "__main__":
    KirixApp().run()

    # Save Settings
    json.dump(settings, open("./.kirix/settings.json", "w"), indent=4)

