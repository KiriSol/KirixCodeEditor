from kivy.uix.boxlayout import BoxLayout

from modules.uix.custom_button.custom_button import CustomButton
from modules.core.get_settings.get_settings import Settings


class ToolBar(BoxLayout):
    children: list[CustomButton]

    def set_settings_and_theme(self) -> None:
        if Settings():
            for ch in self.children:
                ch.set_settings_and_theme()
