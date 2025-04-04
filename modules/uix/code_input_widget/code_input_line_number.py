from typing import Any, Literal
from pygments.lexer import LexerMeta

from kivy.properties import (
    NumericProperty,
    ListProperty,
    StringProperty,
)
from kivy.uix.behaviors import FocusBehavior
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.codeinput import CodeInput

from modules.core.get_settings.get_settings import Settings


class LineNumbers(CodeInput):
    """
    Класс для отображения номеров строк
    """

    START_LINE_NUMBER: Literal[1] = NumericProperty(1)  # Номер первой строки

    text: str
    lines_flags: list[int] = ListProperty([])  # Список флагов перехода на новую строку
    amount_lines: int = NumericProperty(1)

    line_spacing: int
    font_name: str
    font_size: int
    background_color: str | tuple[float, float, float, float]
    foreground_color: str | tuple[float, float, float, float]

    def _update_line_counting(self) -> None:  # Обновление количества строк
        amount_lines: int = self.START_LINE_NUMBER
        text: str = f"{self.START_LINE_NUMBER}"

        for flag in self.lines_flags:
            if flag == CustomCodeInput.LINE_FLAG_NEWLINE:
                amount_lines += 1
                text += f"{amount_lines}\n"
            else:  # Если действует перенос строки
                text += "\n"
        self.amount_lines = amount_lines
        self.text = text

    def on_scroll_y(self, *_) -> None:  # Обновление графики при скролле
        self._update_graphics()

    def on_lines_flags(self, *_) -> None:  # Обновление количества строк
        self._update_line_counting()


class CustomCodeInput(CodeInput):
    """
    CodeInput с дополнительными свойствами и методами
    """

    amount_lines: int = NumericProperty(1)
    lines_flags: list[int] = ListProperty([])

    LINE_FLAG_NEWLINE: Literal[1] = 1  # Флаг перехода на новую строку

    readonly: bool
    focus: bool
    font_name: str
    font_size: int
    line_spacing: int
    tab_width: int
    background_color: str | tuple[float, float, float, float]
    foreground_color: str | tuple[float, float, float, float]
    cursor_color: str | tuple[float, float, float, float]
    selection_color: str | tuple[float, float, float, float]

    def on__lines(self, *_) -> None:  # Обновление количества строк
        amount_lines = 1
        self.lines_flags = self._lines_flags
        for flag in self.lines_flags:
            if flag == self.LINE_FLAG_NEWLINE:
                amount_lines += 1
        self.amount_lines = amount_lines

    def on_scroll_y(self, *_) -> None:  # Обновление графики при скролле
        self._update_graphics()

    # region
    # --------------------------------------
    #           Не задействовано
    # --------------------------------------

    # Переход к нужной строке
    # def go_to_line(self, line_number: int) -> None:
    #     self.cursor: tuple[Literal[0], int] = (0, 0)
    #     self.cursor_line = 1
    #     flag_index = 0
    #     while self.cursor_line < line_number - 1:
    #         if self.lines_flags[flag_index] == self.LINE_FLAG_NEWLINE:
    #             self.cursor_line += 1
    #         flag_index += 1
    #     # sometimes we get 1 line before the intended line
    #     if not self.lines_flags[flag_index] == self.LINE_FLAG_NEWLINE:
    #         flag_index += 1
    #     self.cursor = (0, flag_index)

    # endregion


class CodeInputLineNumber(FocusBehavior, BoxLayout):
    text_content: CustomCodeInput
    line_numbers: LineNumbers

    scroll_y: int = NumericProperty(0)
    amount_lines: int = NumericProperty(1)
    lines_flags: list = ListProperty([])

    text: str = StringProperty("")
    selection: str = StringProperty("")
    cursor: list[int]

    lexer: LexerMeta

    readonly: bool
    on_focus: bool

    line_spacing: int
    tab_size: int
    font_size: int
    font_name: str

    background_color: str | tuple[float, float, float, float]
    foreground_color: str | tuple[float, float, float, float]
    cursor_color: str | tuple[float, float, float, float]
    selection_color: str | tuple[float, float, float, float]

    def set_settings_and_theme(self) -> None:
        if Settings():
            self.line_spacing = Settings()["UI"]["Editor"]["line_spacing"]
            self.font_name = Settings()["UI"]["Editor"]["font"]
            self.font_size = Settings()["UI"]["Editor"]["font_size"]
            self.tab_size = Settings()["UI"]["Editor"]["tab_size"]

            theme: dict[str, Any] = Settings()["Themes"][Settings()["theme"]]
            self.background_color = theme["background"]
            self.foreground_color = theme["foreground"]
            self.cursor_color = theme["cursor"]
            self.selection_color = theme["selection"]

    def update_graphics(self) -> None:
        self.line_numbers._update_graphics()
        self.text_content._update_graphics()

    def set_cursor_line(self, cursor_line: int) -> None:
        self.cursor = [0, cursor_line]
    
    def insert_text(self, text: str) -> None:
        self.text_content.insert_text(text)

    # --------------------------------------
    #           Не задействовано
    # --------------------------------------

    # TODO: Переписать && дополнить методы

