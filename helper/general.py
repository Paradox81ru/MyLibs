import ctypes
import logging
import re
import time
from dataclasses import dataclass
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
            int(value)
            return True
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
            raise ValueError(f"The value field '{self.name}' can only be int.")
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
    Сравнивает два списка
    :param list_1: список 1
    :param list_2: список 2
    :return: одинаковы ли список
    >>> a = ['a','b', 'c', 'd']
    >>> b = ['a','b', 'c', 'd']
    >>> c = ['a', 'c', 'd', 'e']
    >>> comparing_two_lists(a, b)
    True
    >>> comparing_two_lists(a, c)
    False
    """
    return all(map(lambda a, b: a == b, list_1, list_2))
