from typing import Literal, Any, assert_never

import enum

from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput

from modules.core.get_settings.get_settings import Settings


class PushMessage(Popup):
    class TypeMessage(enum.Enum):
        INFO = 0
        WARNING = 1
        ERROR = 2

    TITLES_OF_TYPE: dict[TypeMessage, Literal["Info:", "Warning!", "Error!"]] = dict(
        zip(TypeMessage, ["Info:", "Warning!", "Error!"])
    )
    title: Literal["Info:", "Warning!", "Error!"]
    type_message: TypeMessage

    separator_color: str | tuple[float, float, float, float]
    title_color: str | tuple[float, float, float, float]
    foreground_color: str | tuple[float, float, float, float]
    background_color: str | tuple[float, float, float, float]

    label: TextInput
    text: str
    font: str
    title_font: str

    font_size: float
    title_font_size: float
    line_spacing: float

    background: str

    def __init__(
        self,
        text: str = "",
        *,
        type_message: Literal["info", "warning", "error"] = "info",
        get_settings: bool = True,
        settings: dict[str, Any] | Settings | None = None,
        **kwargs: dict[str, Any],
    ) -> None:
        super().__init__(**kwargs)
        self.set_type(type_message)
        self.title = self.TITLES_OF_TYPE[self.type_message]
        self.text = text
        self.label.cursor = [0, 0]

        if get_settings and not settings:
            settings = Settings()

        self.set_settings_and_theme(settings)

    def show_message(self, message: str = "") -> None:
        if message != "":
            self.text = message
        self.open()
        print(self.text)

    def set_type(self, type: Literal["info", "warning", "error"] = "info") -> None:
        match type:
            case "info":
                self.type_message = self.TypeMessage.INFO
            case "warning":
                self.type_message = self.TypeMessage.WARNING
            case "error":
                self.type_message = self.TypeMessage.ERROR
            case _ as unreachable:
                assert_never(unreachable)

    def set_settings_and_theme(
        self, settings: dict[str, Any] | Settings | None = None
    ) -> None:
        self.foreground_color = "#FFFFFF"  # TODO: исправить костыль
        if settings:
            self.font = settings["UI"]["PushMessage"]["font"]
            self.font_size = settings["UI"]["PushMessage"]["font_size"]
            self.title_font = settings["UI"]["Buttons"]["font"]
            self.title_font_size = settings["UI"]["PushMessage"]["title_font_size"]
            self.line_spacing = settings["UI"]["PushMessage"]["line_spacing"]

            theme: dict[str, Any] = settings["Themes"][settings["theme"]]
            match self.type_message:
                case self.TypeMessage.INFO:
                    self.title_color = theme["PushMessage"]["info"]["title"]
                    self.separator_color = theme["PushMessage"]["info"]["separator"]
                    self.background_color = theme["PushMessage"]["info"]["background"]
                    self.foreground_color = theme["PushMessage"]["info"]["foreground"]
                case self.TypeMessage.WARNING:
                    self.title_color = theme["PushMessage"]["warning"]["title"]
                    self.separator_color = theme["PushMessage"]["warning"]["separator"]
                    self.background_color = theme["PushMessage"]["warning"][
                        "background"
                    ]
                    self.foreground_color = theme["PushMessage"]["warning"][
                        "foreground"
                    ]
                case self.TypeMessage.ERROR:
                    self.title_color = theme["PushMessage"]["error"]["title"]
                    self.separator_color = theme["PushMessage"]["error"]["separator"]
                    self.background_color = theme["PushMessage"]["error"]["background"]
                    self.foreground_color = theme["PushMessage"]["error"]["foreground"]
                case _ as unreachable:
                    assert_never(unreachable)
