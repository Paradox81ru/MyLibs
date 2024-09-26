def cached_reader(fn):
    """ Декоратор для кэшера """
    def func(self, *args, **kwargs):
        if fn.__name__ not in self._cache:
            self._cache[fn.__name__] = fn(self, *args, **kwargs)
        return self._cache[fn.__name__]
    return func


class CacheReaderClass:
    """ Класс кэшер """
    def __init__(self):
        self._cache = {}

    def _cached_reader(self, key: str, func: callable, *args, **kwargs):
        """ Читает значение переменной из кэша """
        if key not in self._cache:
            self._cache[key] = func(*args, **kwargs)
        return self._cache[key]


class MyClass(CacheReaderClass):
    def _a_value(self):
        print('Calc a_value')
        return 20 * 5

    def _b_value(self, x):
        print('Calc b_value')
        return 20 * x

    @property
    def a_value(self):
        return self._cached_reader('a_value', self._a_value)

    @property
    def b_value(self):
        return self._cached_reader('b_value', self._b_value, 7)

    @property
    @cached_reader
    def x_value(self):
        print(f'Calc x_value')
        return 50 + 7

    @cached_reader
    def y_value(self, a):
        print('Calc y_value')
        return 50 + a


def main():
    my_class = MyClass()
    a = my_class.a_value
    print(str(a))
    b = my_class.a_value
    print(str(b))
    c = my_class.a_value
    print(str(c))
    print("")

    a1 = my_class.b_value
    print(str(a1))
    b1 = my_class.b_value
    print(str(b1))
    c1 = my_class.b_value
    print(str(c1))
    print("")

    a2 = my_class.x_value
    print(str(a2))
    b2 = my_class.x_value
    print(str(b2))
    c2 = my_class.x_value
    print(str(c2))
    print("")

    a3 = my_class.y_value(3)
    print(str(a3))
    b3 = my_class.y_value(3)
    print(str(b3))
    c3 = my_class.y_value(3)
    print(str(c3))


if __name__ == '__main__':
    main()
