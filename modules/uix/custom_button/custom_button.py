from typing import Any

from kivy.uix.button import Button

from modules.core.get_settings.get_settings import Settings


class CustomButton(Button):
    font: str
    font_size: float
    background_color: str | tuple[float, float, float, float]
    text_color: str | tuple[float, float, float, float]
    background_normal: str
    background_down: str

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

    def set_settings_and_theme(self) -> None:
        if Settings():
            self.font = Settings()["UI"]["Buttons"]["font"]
            self.font_size = Settings()["UI"]["Buttons"]["font_size"]

            theme: dict[str, Any] = Settings()["Themes"][Settings()["theme"]]
            self.background_color = theme["Buttons"]["background"]
            self.text_color = theme["Buttons"]["text_color"]
            self.background_normal = theme["Buttons"]["background_normal"]
            self.background_down = theme["Buttons"]["background_down"]
