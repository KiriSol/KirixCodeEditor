from typing import Any, Literal

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput

from modules.core.get_settings.get_settings import Settings
from modules.uix.custom_button.custom_button import CustomButton

# TODO: Сделать btn_open необязательным (Включение/Выключение через настройки)


class PathInput(BoxLayout):
    class CustomTextInput(TextInput):
        def keyboard_on_key_down(
            self, window, keycode, text, modifiers
        ) -> None | Literal[True]:
            if keycode[1] == "enter":
                self.parent.open()
            return super().keyboard_on_key_down(window, keycode, text, modifiers)

    text_input: CustomTextInput
    btn_open: CustomButton

    font: str
    font_size: float
    foreground_color: tuple[float, float, float, float]
    background_color: tuple[float, float, float, float]

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

    # TODO: исправить костыль (обязательное расположение в root)
    def open(self) -> None:
        self.parent.parent.open(self.get_path())

    def set_settings_and_theme(self) -> None:
        if Settings():
            self.font = Settings()["UI"]["PathInput"]["font"]
            self.font_size = Settings()["UI"]["PathInput"]["font_size"]

            theme: dict[str, Any] = Settings()["Themes"][Settings()["theme"]]
            self.foreground_color = theme["foreground"]
            self.background_color = theme["background"]

            self.btn_open.set_settings_and_theme()

    def get_path(self) -> str:
        return self.text_input.text

    def set_path(self, path: str) -> None:
        self.text_input.text = path
