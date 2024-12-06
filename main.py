from io import TextIOWrapper
import os
import json

# Kivy
from kivy.app import App
from kivy.properties import ObjectProperty, StringProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.lang.builder import Builder

# My Modules
from Components.TextLine.textinputlinenumber import TextInputLineNumber

# KV
Builder.load_file("./kv/codeeditor.kv")
Builder.load_file("./kv/textinputlinenumber.kv")

os.makedirs("./.kirix", exist_ok=True)

# Open Settings
settings = json.load(open("./.kirix/settings.json", "r"))
file_path = settings["path_file"]




class CodeEditorRoot(BoxLayout):
    pass


class CodeEditorApp(App):
    def build(self):
        return CodeEditorRoot()


if __name__ == "__main__":

    CodeEditorApp().run()

    # Save Settings
    json.dump(settings, open("./.kirix/settings.json", "w"))
