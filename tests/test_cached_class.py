import pytest

from helper.cached_class import CachedReader, cached_reader


class MyClass(CachedReader):
    def _a_value(self):
        print('Calc a_value')
        return 20 * 5

    def _b_value(self, x):
        print('Calc b_value')
        return 20 * x

    @property
    def a_value(self):
        return self._cached_reader(self._a_value)

    @property
    def b_value(self):
        return self._cached_reader(self._b_value, 7)

    @property
    @cached_reader
    def x_value(self):
        print(f'Calc x_value')
        return 50 + 7

    @cached_reader
    def y_value(self, a):
        print('Calc y_value')
        return 50 + a

    @cached_reader
    def z_value(self, a, *, b):
        print('Calc z_value')
        return 50 * a + b


def test_cache_reader_class(capsys):
    my_class = MyClass()
    a = my_class.a_value
    captured = capsys.readouterr()
    assert a == 100
    assert captured.out == "Calc a_value\n"
    b = my_class.b_value
    captured = capsys.readouterr()
    assert b == 140
    assert captured.out == "Calc b_value\n"

    a1 = my_class.a_value
    captured = capsys.readouterr()
    assert a1 == a
    assert captured.out == ""
    b1 = my_class.b_value
    captured = capsys.readouterr()
    assert b1 == b
    assert captured.out == ""

    my_class.cache_reset('_a_value')
    a3 = my_class.a_value
    captured = capsys.readouterr()
    assert a3 == a
    assert captured.out == "Calc a_value\n"
    b3 = my_class.b_value
    captured = capsys.readouterr()
    assert b3 == b
    assert captured.out == ""

    my_class.cache_reset()
    a4 = my_class.a_value
    captured = capsys.readouterr()
    assert a4 == a
    assert captured.out == "Calc a_value\n"
    b4 = my_class.b_value
    captured = capsys.readouterr()
    assert b4 == b
    assert captured.out == "Calc b_value\n"

    a5 = my_class.a_value
    captured = capsys.readouterr()
    assert a5 == a
    assert captured.out == ""
    b5 = my_class.b_value
    captured = capsys.readouterr()
    assert b5 == b
    assert captured.out == ""

    x = my_class.x_value
    captured = capsys.readouterr()
    assert x == 57
    assert captured.out == "Calc x_value\n"
    x2 = my_class.x_value
    captured = capsys.readouterr()
    assert x2 == x
    assert captured.out == ""

    y11 = my_class.y_value(3)
    captured = capsys.readouterr()
    assert y11 == 53
    assert captured.out == "Calc y_value\n"
    y12 = my_class.y_value(3)
    captured = capsys.readouterr()
    assert y12 == y11
    assert captured.out == ""

    y21 = my_class.y_value(5)
    captured = capsys.readouterr()
    assert y21 == 55
    assert captured.out == "Calc y_value\n"
    y22 = my_class.y_value(5)
    captured = capsys.readouterr()
    assert y22 == y21
    assert captured.out == ""

    z = my_class.z_value(2, b=3)
    captured = capsys.readouterr()
    assert z == 103
    assert captured.out == "Calc z_value\n"
    z1 = my_class.z_value(2, b=3)
    captured = capsys.readouterr()
    assert z1 == z
    assert captured.out == ""

    z2 = my_class.z_value(3, b=2)
    captured = capsys.readouterr()
    assert z2 == 152
    assert captured.out == "Calc z_value\n"
    z3 = my_class.z_value(3, b=2)
    captured = capsys.readouterr()
    assert z3 == z2
    assert captured.out == ""

    # Сбрасывается кэш только для указанных аргументов.
    my_class.cache_reset('z_value_2_b=3')
    z4 = my_class.z_value(2, b=3)
    captured = capsys.readouterr()
    assert z4 == z
    assert captured.out == "Calc z_value\n"
    z3 = my_class.z_value(3, b=2)
    captured = capsys.readouterr()
    assert z3 == z2
    assert captured.out == ""
    z1 = my_class.z_value(2, b=3)
    captured = capsys.readouterr()
    assert z1 == z
    assert captured.out == ""

    # Сбрасывает кэш сразу для всех аргументов функции
    my_class.cache_reset('z_value', is_match=False)
    z = my_class.z_value(2, b=3)
    captured = capsys.readouterr()
    assert z == 103
    assert captured.out == "Calc z_value\n"
    z1 = my_class.z_value(2, b=3)
    captured = capsys.readouterr()
    assert z1 == z
    assert captured.out == ""
    z2 = my_class.z_value(3, b=2)
    captured = capsys.readouterr()
    assert z2 == 152
    assert captured.out == "Calc z_value\n"
    z3 = my_class.z_value(3, b=2)
    captured = capsys.readouterr()
    assert z3 == z2
    assert captured.out == ""

