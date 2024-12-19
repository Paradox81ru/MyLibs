import random
import time
from functools import partial

import pytest

from helper.general import variation_of_number, pack_string, unpack_string, comparing_two_lists, repeat_attempts, \
    RunFunction, DescriptorOnlyInt


class ClassDescriptorOnlyInt:
    x = 4
    y = DescriptorOnlyInt()


def test_descriptor_only_int():
    """ Проверяет работу дескриптора, обеспечивающего проверка на только целое число """
    instance_descriptor_only_int = ClassDescriptorOnlyInt()
    instance_descriptor_only_int.x = 5
    instance_descriptor_only_int.y = 7
    with pytest.raises(ValueError) as ex_info:
        instance_descriptor_only_int.y = 5.7
    assert ex_info.value.args[0] == "Error value=5.7. The value field 'y' can only be int."

    with pytest.raises(ValueError) as ex_info:
        instance_descriptor_only_int.y = "f"
    assert ex_info.value.args[0] == "Error value=f. The value field 'y' can only be int."


def attempts_random_func(_min, _max):
    """ Функция для случайного повторения попыток """
    return random.randint(_min, _max)


class AttemptsSuccessiveClass:
    """ Класс для последовательного повторения попыток """
    def __init__(self, pause: float = 0):
        self._pause = pause
        self._current_num = 0

    def __call__(self, *args, **kwargs):
        time.sleep(self._pause)
        self._current_num += 1
        return self._current_num


@pytest.mark.skip(reason="Unclear behavior of function processing time")
def test_repeat_attempts():
    """ Тестирует функцию повторение попыток исполнения функции до истечения указанного времени """
    # region
    err_msg_1 = "The time of attempts exceeds the allowed time"
    err_msg_2 = "The function 'repeat_attempts' did not return a value"
    func_1 = partial(attempts_random_func, 0, 100)
    end_time = time.monotonic() + 1.1
    a = repeat_attempts(func_1, lambda x: x > 80)
    # Проверяется, что время ожидание было не больше 1-оё секунды.
    assert time.monotonic() < end_time, err_msg_1
    assert isinstance(a, int), err_msg_2

    func_2 = RunFunction(attempts_random_func, [0, 100], None)
    end_time = time.monotonic() + 1.1
    b = repeat_attempts(func_2, lambda x: x < 20)
    # Проверяется, что время ожидание было не больше 1-оё секунды.
    assert time.monotonic() < end_time, err_msg_1
    assert isinstance(b, int), err_msg_2

    func_3 = RunFunction(attempts_random_func, [0, 80], None)
    begin_time = time.monotonic()
    with pytest.raises(TimeoutError) as ex_info:
        _ = repeat_attempts(func_3, lambda x: x > 80, 3)
    # Проверяется, что время ожидание было 3 секунды, пока не сработала ошибка.
    assert 3 < (time.monotonic() - begin_time) < 4, err_msg_1
    assert str(ex_info.value) == "Error. The time for attempts to execute the function has expired"

    func_4 = AttemptsSuccessiveClass(0.01)
    begin_time = time.monotonic()
    d = repeat_attempts(func_4, lambda x: x > 100, 2)
    # Проверяется, что функция отработала в пределах от 1,5 до 2.5 секунд
    assert 1.5 < (time.monotonic() - begin_time) < 2.5, err_msg_1
    assert isinstance(d, int), err_msg_2

    func_5 = AttemptsSuccessiveClass(0.05)
    begin_time = time.monotonic()
    with pytest.raises(TimeoutError) as ex_info:
        _ = repeat_attempts(func_5, lambda x: x > 150, 2,
                                       "The waiting time for the correct value has exceeded 2 seconds")
        # Проверяется, что функция отработала в пределах от 1,5 до 2.5 секунд
    assert 2 < (time.monotonic() - begin_time) < 3, err_msg_1
    assert str(ex_info.value) == "The waiting time for the correct value has exceeded 2 seconds"
    # endregion


_one_list = ['a','b', 'c', 'd']
_two_list = ['a','b', 'c', 'd']
_three_list = ['a', 'c', 'd', 'e']


@pytest.mark.parametrize("one_list, two_list, result", (
        (_one_list, _two_list, True),
        (_one_list, _three_list, False)
))
def test_comparing_two_lists(one_list, two_list, result):
    assert comparing_two_lists(one_list, two_list) is result


def test_pack_unpack_string(tmp_path):
    """ Проверяет запаковку строки в байтовый массив и распаковку обратно. """
    string_to_pack = "Pack string 123"
    temp_dir = tmp_path / 'to_pack_string'
    temp_dir.mkdir()
    temp_file = temp_dir / 'file_to_pack_string.tmp'
    with open(temp_file, "wb") as f:
        pack_bytes = pack_string(string_to_pack)
        f.write(pack_bytes)

    with open(temp_file, "rb") as f:
        string_unpack = unpack_string(f)

    assert string_unpack == string_to_pack


def idfn(val):
    return val if isinstance(val, int) else ""


@pytest.mark.parametrize("number, result", (
    (0, "Домов"), (1, "Дом"), (2, "Дома"), (3, "Дома"), (4, "Дома"), (5, "Домов"), (6, "Домов"),
    (10, "Домов"), (11, "Домов"), (13, "Домов"), (19, "Домов"), (20, "Домов"),
    (21, "Дом"), (22, "Дома"), (24, "Дома"), (25, "Домов"), (29, "Домов"), (30, "Домов"),
    (99, "Домов"), (100, "Домов"), (101, "Дом"), (102, "Дома"), (105, "Домов"),
    (-1, "Дом"), (-2, "Дома"), (-3, "Дома"), (-5, "Домов")
), ids=idfn)
def test_variation_of_number(number, result):
    """ Проверяет склонение слова в зависимости от указанного числа """
    root_word = "Дом"
    one_end = ""
    two_end = "а"
    three_end = "ов"
    assert variation_of_number(number, root_word, one_end, two_end, three_end) == result


@pytest.mark.parametrize("number, result", (
    (0, "Крыс"), (1, "Крыса"), (2, "Крысы"), (3, "Крысы"), (4, "Крысы"), (5, "Крыс"), (6, "Крыс"),
    (10, "Крыс"), (11, "Крыс"), (13, "Крыс"), (19, "Крыс"), (20, "Крыс"),
    (21, "Крыса"), (22, "Крысы"), (24, "Крысы"), (25, "Крыс"), (29, "Крыс"), (30, "Крыс"),
    (99, "Крыс"), (100, "Крыс"), (101, "Крыса"), (102, "Крысы"), (105, "Крыс"),
    (-1, "Крыса"), (-2, "Крысы"), (-3, "Крысы"), (-5, "Крыс")
), ids=idfn)
@pytest.mark.params()
def test_variation_of_number_2(number, result):
    """ Проверяет склонение другого слова в зависимости от указанного числа """
    root_word = "Крыс"
    one_end = "а"
    two_end = "ы"
    three_end = ""
    assert variation_of_number(number, root_word, one_end, two_end, three_end) == result
