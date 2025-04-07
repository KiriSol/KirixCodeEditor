import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from typing import Any

from kivy.app import App

from kivy.uix.boxlayout import BoxLayout

from kivy.factory import Factory

from modules.uix.code_input_to_file.code_input_file import CodeInputToFile
from modules.uix.path_input.path_input import PathInput
from modules.uix.tool_bar.tool_bar import ToolBar
from modules.uix.push_message.push_message import PushMessage

from modules.core.get_settings.get_settings import Settings

Factory.register("PushMessage", PushMessage)


__version__ = "0.1.0"


class KirixCodeRoot(BoxLayout):
    code_input: CodeInputToFile
    path_input: PathInput
    tool_bar: ToolBar

    def __init__(self, **kwargs: dict[str, Any]) -> None:
        super().__init__(**kwargs)

    def open(self, path: str = "$welcome") -> None:
        self.code_input.open(path)

    def save(self) -> None:
        self.code_input.save()

    def delete(self) -> None:
        self.code_input.delete()

    def run(self) -> None:
        self.code_input.run()

    def load_settings(self) -> None:
        if Settings():
            for ch in self.children:
                ch.set_settings_and_theme()

    def reload_settings(self) -> None:
        Settings().reload_settings()
        self.load_settings()


class KirixCodeApp(App):
    root: KirixCodeRoot

    def __init__(self, **kwargs: dict[str, Any]) -> None:
        super().__init__(**kwargs)

    def build(self) -> ...:
        return KirixCodeRoot()

    def on_start(self) -> None:
        self.root.load_settings()
        self.root.open()


def main() -> None:
    KirixCodeApp().run()


if __name__ == "__main__":
    main()
