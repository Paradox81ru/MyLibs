import json
from typing import Iterable

from jsonpath_ng.ext import parse
from jsonpath_ng import Descendants


def json_converter_to_lofl(_json: str | dict | list) -> list[list]:
    """ Преобразует JSON в список списков. """
    def convert(val):
        return sorted([(item[0], convert(item[1])) for item in val.items()]) if isinstance(val, dict) \
            else val if isinstance(val, str) else sorted([convert(item) for item in val]) if isinstance(val, Iterable) \
            else val

    if isinstance(_json, str):
        _obj = json.loads(_json)
    elif isinstance(_json, dict) or isinstance(_json, list):
        _obj = _json
    else:
        raise TypeError("JSON must be provided either as a string or as type Dict, list or tuple")

    return convert(_obj)


def compare_json(json_1: str | dict | list, json_2: str | dict | list, str_xpath: str = None):
    """
    Проверка вхождения str_json_1 в str_json_2.
    :param json_1: json который проверяется.
    :param json_2: json с которым проверяется.
    :param str_xpath: Строка xpath для выбирания нужных узлов из JSON.
    :return:
    """
    def get_hash(_json, _str_xpath):
        """
        Возвращает однозначный HASH строки json.
        :param _json: Строка JSON.
        :param _str_xpath: Строка xpath для выбирания нужных узлов из JSON.
        :return: Список HASH-сумм переданного JSON.
        """
        # Строка JSON преобразуется в объект, если быа передана строка.
        _json = json.loads(_json) if isinstance(_json, str) else _json
        # Производится поиск указанных в XPATH узлов.
        jpe: Descendants = parse(_str_xpath)
        json_list: list = jpe.find(_json)
        # Формируется список строк найденных узлов преобразованных в список списков.
        if len(json_list) > 1:
            json_str_lofl = [json_converter_to_lofl(item.value) for item in json_list]
        else:
            # Берётся список из значения, если значением является список,
            # а если это словарь, то словарь разбивается в список.
            json_list = json_list[0].value if isinstance(json_list[0].value, list) \
                else [{key: val} for key, val in json_list[0].value.items()]
            json_str_lofl = list(map(json_converter_to_lofl, json_list))
        # logger.debug(f"JSON string with XPATH '{_str_xpath}': {json_str_lofl}")
        # Текстовые строки списка списков преобразуются в HASH-и.
        return list(map(lambda i: hash(repr(i)), json_str_lofl))

    # Если xpath не указан, то сравнивается весь JSOn.
    if str_xpath is None:
        json_1_lofl = json_converter_to_lofl(json_1)
        # logger.debug(f"JSON string 1: {json_1_lofl}")
        hash_json_str_1 = hash(repr(json_1_lofl))

        json_2_lofl = json_converter_to_lofl(json_2)
        # logger.debug(f"JSON string 2: {json_2_lofl}")
        hash_json_str_2 = hash(repr(json_2_lofl))
        return hash_json_str_1 == hash_json_str_2
    else:
        json_hash_list_1 = get_hash(json_1, str_xpath)
        json_hash_list_2 = get_hash(json_2, str_xpath)
        return all(map(lambda i: any(map(lambda j: j == i, json_hash_list_2)), json_hash_list_1))


def convert_response_to_string(response: str | dict | list, is_formatted: bool = False):
    """
    Конвертирует JSON-ответ в строку.
    :param response: Отвёт в формате JSON или строки.
    :param is_formatted: Должен ли ответ быть отформатирован.
    :return:
    """
    if not(isinstance(response, str) or isinstance(response, dict) or isinstance(response, list)):
        raise ValueError("the response must be in string or dictionary or list format")
    # Если ответ должен быть отформатирован,
    if is_formatted:
        # то вначале строковый вариант ответа надо преобразовать в JSON,
        # только его потом можно отформатировать.
        if isinstance(response, str):
            response = json.loads(response
                                       .replace("'", '"')
                                       .replace('True', 'true')
                                       .replace('False', 'false'))
        response = json.dumps(response, indent=2)
    return str(response)
