from typing import Any

import os
import json
from jsonschema import validate, ValidationError

from kivy.factory import Factory

from data import PACKAGE_PATH


def merge_2_nested_dict(
    dict_default: dict[Any, Any],
    dict_force: dict[Any, Any],
) -> dict[Any, Any]:
    """Слияние двух вложенных словарей в один

    Args:
        dict_default (dict[Any, Any]): словарь по умолчанию
        dict_force (dict[Any, Any]): приоритетный словарь

    Returns:
        dict[Any, Any]: объединенный словарь
    """

    res_dict_level: dict[Any, Any] = dict_default | dict_force
    for k in res_dict_level.keys():
        if isinstance(dict_default.get(k), dict) and isinstance(
            dict_force.get(k), dict
        ):
            res_dict_level[k] = merge_2_nested_dict(dict_default[k], dict_force[k])
        elif isinstance(dict_default.get(k), list) and isinstance(
            dict_force.get(k), list
        ):
            for i in dict_default[k]:
                if i not in dict_force[k]:
                    res_dict_level[k].append(i)

    return res_dict_level


class Singleton(type):
    _instances: dict[Any, Any] = {}

    def __call__(cls, *args, **kwargs) -> Any:
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class Settings(dict, metaclass=Singleton):
    """Класс настроек приложения (один экземпляр), наследуется от dict"""

    is_content: bool

    def __init__(self) -> None:
        self._set_settings()

    def _set_settings(self) -> None:
        self.is_content = False
        # Получение настроек
        try:
            default_settings: dict[str, Any] = json.load(
                open(f"{PACKAGE_PATH}/kirix/default_settings.json")
            )
            default_settings_schema: dict[str, Any] = json.load(
                open(f"{PACKAGE_PATH}/kirix/default_settings_schema.json")
            )
            user_settings: dict[str, Any] = json.load(
                open(f"{PACKAGE_PATH}/kirix/user_settings.json")
            )
            user_settings_schema: dict[str, Any] = json.load(
                open(f"{PACKAGE_PATH}/kirix/user_settings_schema.json")
            )
        except FileNotFoundError as err:
            Factory.PushMessage(
                f"Настройки не найдены (Попробуйте переустановить приложение):\n{err}",
                type_message="error",
                get_settings=False,
            ).show_message()
            return
        except json.decoder.JSONDecodeError as err:
            Factory.PushMessage(
                f"Настройки повреждены:\n{err}",
                type_message="error",
                get_settings=False,
            ).show_message()
            return
        except Exception as err:
            Factory.PushMessage(
                f"Что-то пошло не так:\n{err}", type_message="error", get_settings=False
            ).show_message()
            return

        try:  # проверяем настройки по умолчанию
            validate(default_settings, default_settings_schema)
        except ValidationError as err:
            Factory.PushMessage(
                f"Настройки по умолчанию повреждены:\n{err}",
                type_message="error",
                get_settings=False,
            ).show_message()
            return

        for k in default_settings["UI"].keys():
            for path in default_settings["search_paths"]:
                if os.path.exists(path + "/" + default_settings["UI"][k]["font"]):
                    default_settings["UI"][k]["font"] = (
                        path + "/" + default_settings["UI"][k]["font"]
                    )
                    break
                elif os.path.exists(
                    path + "/" + default_settings["UI"][k]["font"] + ".ttf"
                ):
                    default_settings["UI"][k]["font"] = (
                        path + "/" + default_settings["UI"][k]["font"] + ".ttf"
                    )
                    break
                elif os.path.exists(default_settings["UI"][k]["font"]):
                    break
            else:  # Если не нашли ни одного шрифта
                Factory.PushMessage(
                    f"Ошибка в настройках по умолчанию:\nПуть к шрифту {default_settings['UI'][k]['font']} не найден, используется шрифт по умолчанию.!!!",
                    type_message="error",
                    get_settings=False,
                ).show_message()
                default_settings["UI"][k]["font"] = "Roboto"

        if default_settings["theme"] not in default_settings["Themes"].keys():
            Factory.PushMessage(
                f"Ошибка в настройках по умолчанию:\nТема {default_settings['theme']} не найдена",
                type_message="error",
                get_settings=False,
            )
            return

        self.is_content = True
        self.update(default_settings)

        try:  # проверяем пользовательские настройки
            validate(user_settings, user_settings_schema)
        except ValidationError as err:
            Factory.PushMessage(
                f"Вы ввели некорректные пользовательские настройки:\n{err}",
                type_message="error",
                settings=self,
            ).show_message()
            return

        # Объединяем настройки
        settings: dict[str, Any] = merge_2_nested_dict(default_settings, user_settings)

        # Проверяем настройки
        if settings["theme"] not in settings["Themes"].keys():
            settings["theme"] = default_settings["theme"]
            Factory.PushMessage(
                f"Тема {settings['theme']} не найдена, используется тема {default_settings['theme']}.",
                type_message="warning",
                settings=self,
            ).show_message()
        if settings["RESERVED_PATHS"] != default_settings["RESERVED_PATHS"]:
            Factory.PushMessage(
                "Зарезервированные пути были изменены.",
                type_message="warning",
                settings=self,
            ).show_message()
            self.update(default_settings)
            return

        for path in settings["user_aliases"].keys():
            if not os.path.exists(settings["user_aliases"][path]):
                Factory.PushMessage(
                    f"Путь по псевдониму {path} ({settings['user_aliases'][path]}) не найден",
                    type_message="warning",
                    settings=self,
                ).show_message()

        for k in settings["UI"].keys():
            for path in settings["search_paths"]:
                if os.path.exists(path + "/" + settings["UI"][k]["font"]):
                    settings["UI"][k]["font"] = path + "/" + settings["UI"][k]["font"]
                    break
                elif os.path.exists(path + "/" + settings["UI"][k]["font"] + ".ttf"):
                    settings["UI"][k]["font"] = (
                        path + "/" + settings["UI"][k]["font"] + ".ttf"
                    )
                    break
                elif os.path.exists(settings["UI"][k]["font"]):
                    break
                elif settings["UI"][k]["font"] == "Roboto":
                    break
            else:  # Если не нашли ни одного шрифта
                Factory.PushMessage(
                    f"Путь к шрифту {settings['UI'][k]['font']} не найден, используется шрифт по умолчанию.",
                    type_message="warning",
                    settings=self,
                ).show_message()
                settings["UI"][k]["font"] = default_settings["UI"][k]["font"]
                return

        for k in settings["Themes"].keys():
            settings["Themes"][k] = merge_2_nested_dict(
                default_settings["Themes"]["Default"], settings["Themes"][k]
            )

        self.update(settings)

        if self["report_successful_download"]:
            Factory.PushMessage(
                "Настройки успешно получены.", type_message="info", settings=self
            ).show_message()

    def reload_settings(self) -> None:
        self._set_settings()

    def __bool__(self) -> bool:
        return self.is_content
