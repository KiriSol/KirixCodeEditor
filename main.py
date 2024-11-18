from kivy.app import App
from kivy.properties import ObjectProperty, StringProperty
from kivy.uix.boxlayout import BoxLayout

from TextLine.textinputlinenumber import TextInputLineNumber
from pygments.lexers.c_cpp import CppLexer

class ExampleRoot(BoxLayout):
    lni = ObjectProperty(None)
    text = StringProperty("")

    def append_lorem_ipsum(self, instance=None):
        self.lni.text = ""
        self.lni.text_content.focus = True


    def save(self, instance=None):
        with open("save.py", "w") as file:
            file.write(self.lni.text)
        
    def tab(self, instance=None):
        self.lni.text_content.insert_text("\t")
        self.lni.text_content.focus = True


class CodeEditorApp(App):

    def build(self):
        res = BoxLayout()

        # res.add_widget(BoxLayout(orientation="vertical", size_hint=(0.1, 1)))
        root = ExampleRoot()
        # root.lni.
        try:
            with open("save.py", "r") as file:
                root.lni.text = file.read()
        except FileNotFoundError:
            with open("save.py", "w") as file:
                file.write("print('Hello World!')")
                # for i in range(1_000):
                #     file.write("\n")

        with open("save.py", "r") as file:
            root.lni.text = file.read()
        res.add_widget(root)
        return res


if __name__ == "__main__":
    CodeEditorApp().run()
