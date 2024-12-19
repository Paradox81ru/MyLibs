import ctypes
import logging
import re
import struct
import time
from dataclasses import dataclass
from datetime import datetime
from functools import partial
from pathlib import Path
from typing import Callable


@dataclass
class RunFunction:
    func: Callable = None
    args: list = None
    kwargs: dict = None


class Validate:
    @staticmethod
    def is_int(value):
        """ Проверяет переменную на целое число """
        try:

            return int(value) - value == 0
        except (ValueError, TypeError):
            return False

    @staticmethod
    def is_email(value):
        """ Проверяет адрес электронной почты """
        return re.match(r'^([a-zA-Z0-9_-]+\.)*[a-zA-Z0-9_-]+@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+)*\.[a-zA-Z]{2,6}$', value)


class DescriptorOnlyInt:
    """ Дескриптор ввода только целочисленных значений """
    def __set_name__(self, owner, name):
        self.name = name

    def __get__(self, instance, owner):
        return instance.__dict__[self.name]

    def __set__(self, instance, value):
        if not Validate.is_int(value):
            raise ValueError(f"Error value={value}. The value field '{self.name}' can only be int.")
        instance.__dict__[self.name] = value


def get_logger(logger_name, filename, *, is_debug_mode):
    """
    Возвращает логгер.
    :param logger_name: Наименование логгера.
    :param filename: Имя файла логгера.
    :param is_debug_mode: Включить ли уровень логгера DEBUG.
    :return:
    """

    logger = logging.getLogger(logger_name)
    logger_handler = logging.FileHandler(filename, mode='a', encoding='utf-8')
    logger_formatter = logging.Formatter("%(name)s %(asctime)s %(levelname)s %(message)s")
    logger_handler.setFormatter(logger_formatter)
    logger.addHandler(logger_handler)
    # self.set_logger_level(logging.ERROR)
    logger.setLevel(logging.DEBUG if is_debug_mode else logging.ERROR)
    return logger


def get_root_path():
    """ Возвращает корневой путь модуля """
    return Path(__file__).resolve().parent


def is_admin():
    """
    Является ли текущий пользователем администратором
    :return:
    """
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except Exception:
        return False


def running_process_as_administrator(full_filename: str):
    """ Запускает приложение от имени администратора """
    res = ctypes.windll.shell32.ShellExecuteW(None, 'runas', full_filename, None, None, 1)
    # ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
    # res = subprocess.run(['runas', full_filename])
    return res


def repeat_attempts(func: Callable | RunFunction, condition: Callable, timeout: float = 1, except_message: str = None):
    """
    Повторение попыток исполнения функции до истечения указанного времени.
    :param func: Функция выполнения.
    :param condition: Условие успешного выполнения функции.
    :param timeout: Время на успешное выполнение функции.
    :param except_message: Сообщение исключения в случае истечения времени попыток.
    :return: Успешный результат выполнения функции.
    :raises ValueError: Неверные параметры переданной функции.
    :raises TimeoutError: Истекло время для повторения количества ошибок.
    """

    if isinstance(func, RunFunction):
        if isinstance(func.func, Callable):
            func = partial(func.func, *func.args, **func.kwargs) \
                if (func.args is not None and isinstance(func.args, list)
                    and func.kwargs is not None and isinstance(func.kwargs, dict)) \
                else partial(func.func, *func.args) if (func.args is not None and isinstance(func.args, list)) \
                else partial(func.func, **func.kwargs) if (func.kwargs is not None and isinstance(func.kwargs, dict)) \
                else func.func if (func.args is None and func.kwargs is None) else None
    if func is None:
        raise ValueError("Invalid parameters of the passed function")

    end_time = time.monotonic() + timeout
    result = func()
    while not condition(result):
        if time.monotonic() > end_time:
            raise TimeoutError("Error. The time for attempts to execute the function has expired"
                               if except_message is None else except_message)
        result = func()
    return result


def comparing_two_lists(list_1: list | tuple, list_2: list | tuple):
    """
    Сравнивает два списка.
    :param list_1: список 1.
    :param list_2: список 2.
    :return: Одинаковы ли список.
    >>> a = ['a','b', 'c', 'd']
    >>> b = ['a','b', 'c', 'd']
    >>> c = ['a', 'c', 'd', 'e']
    >>> comparing_two_lists(a, b)
    True
    >>> comparing_two_lists(a, c)
    False
    """
    return all(map(lambda a, b: a == b, list_1, list_2))


def pack_string(string) -> bytes:
    """
    Запаковывает строку в байтовый массив.
    :param string: Строка данных.
    :return: Байтовый массив.
    """
    data = string.encode('utf8')
    data_length = len(data)
    format_str = f"<H{data_length}s"
    return struct.pack(format_str, data_length, data)


def unpack_string(fh, eof_is_error=True) -> str | None:
    """
    Вытаскивает строку из файла и распаковывает ее.
    :param fh: Дескриптор файла.
    :param eof_is_error: Если true, то в случае не нахождения очередной строки будет ошибка.
    :return: Строка данных.
    """
    uint16 = struct.Struct("<H")
    data_length = fh.read(uint16.size)
    if not data_length:
        if eof_is_error:
            raise ValueError("Отсутствует или поврежден размер строки.")
        return None
    length = uint16.unpack(data_length)[0]
    if length == 0:
        return ""
    data = fh.read(length)
    if not data or len(data) != length:
        raise ValueError("Строка отсутствует или повреждена")
    format_str = f"<{length}s"
    return struct.unpack(format_str, data)[0].decode("utf8")


def translate(string):
    """ Преобразует кирилицу в латиницу. """

    transtable = {
        # Большие буквы
        # three-symbols
        u"Щ": u"Sch",
        # two-symbol
        u"Ё": u"Yo",
        u"Ж": u"Zh",
        u"Ц": u"Ts",
        u"Ч": u"Ch",
        u"Ш": u"Sh",
        u"Ы": u"Yi",
        u"Ю": u"Yu",
        u"Я": u"Ya",
        # one-symbol
        u"А": u"A",
        u"Б": u"B",
        u"В": u"V",
        u"Г": u"G",
        u"Д": u"D",
        u"Е": u"E",
        u"З": u"Z",
        u"И": u"I",
        u"Й": u"J",
        u"К": u"K",
        u"Л": u"L",
        u"М": u"M",
        u"Н": u"N",
        u"О": u"O",
        u"П": u"P",
        u"Р": u"R",
        u"С": u"S",
        u"Т": u"T",
        u"У": u"U",
        u"Ф": u"F",
        u"Х": u"H",
        u"Э": u"E",
        u"Ъ": u"`",
        u"Ь": u"'",
        # Маленькие буквы
        # three-symbols
        u"щ": u"sch",
        # two-symbols
        u"ё": u"yo",
        u"ж": u"zh",
        u"ц": u"ts",
        u"ч": u"ch",
        u"ш": u"sh",
        u"ы": u"yi",
        u"ю": u"yu",
        u"я": u"ya",
        # one-symbol
        u"а": u"a",
        u"б": u"b",
        u"в": u"v",
        u"г": u"g",
        u"д": u"d",
        u"е": u"e",
        u"з": u"z",
        u"и": u"i",
        u"й": u"j",
        u"к": u"k",
        u"л": u"l",
        u"м": u"m",
        u"н": u"n",
        u"о": u"o",
        u"п": u"p",
        u"р": u"r",
        u"с": u"s",
        u"т": u"t",
        u"у": u"u",
        u"ф": u"f",
        u"х": u"h",
        u"э": u"e",
        u"ъ": u"`",
        u"ь": u"'",
    }

    string_symbols = set(string)
    for symb in string_symbols:
        if symb in transtable:
            string = string.replace(symb, transtable[symb])
    return string


def datetime_to_timestamp(date_time: datetime):
    """
    Конвертор из даты-времени в число timestamp.
    :param date_time:
    :return:
    """
    return date_time.timestamp()


def timestamp_to_datetime(timestamp: int):
    """
    Конвертор из числа timestamp в дату-время.
    :param timestamp:
    :return:
    """
    return datetime.fromtimestamp(timestamp)


def variation_of_number(number, root_word, one_end, two_end, three_end):
    """
    Производит склонение указанного слова (корня слова) в зависимости от указанного числа.
    :param number: Число, по которому склоняется слова.
    :param root_word: Корень слова, который должен склоняться.
    :param one_end: Первое окончания слова, в единственном числе.
    :param two_end: Второе окончание слова, от одного до пяти.
    :param three_end: Третье окончание слова от пяти до двадцати.
    :return:
    """
    result_word = root_word
    number_end = int(str(number)[-1])
    if 20 > number > 10 or number_end == 0:
        result_word += three_end
    elif number_end == 1:
        result_word += one_end
    elif number_end < 5:
        result_word += two_end
    else:
        result_word += three_end
    return result_word
