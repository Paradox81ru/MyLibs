def cached_reader(fn):
    """ Декоратор для кэшера """
    def func(self, *args, **kwargs):
        cache_key = fn.__name__
        for arg in args:
            cache_key += f"_{arg}"
        for key, value in kwargs.items():
            cache_key += f"_{key}={value}"
        if cache_key not in self._cache:
            self._cache[cache_key] = fn(self, *args, **kwargs)
        return self._cache[cache_key]
    return func


class CacheReaderClass:
    """ Класс кэшер """
    def __init__(self):
        self._cache = {}

    def _cached_reader(self, func: callable, *args, **kwargs):
        """ Читает значение переменной из кэша """
        cache_key = func.__name__
        for arg in args:
            cache_key += f"_{arg}"
        for key, value in kwargs.items():
            cache_key += f"_{key}={value}"
        if cache_key not in self._cache:
            self._cache[cache_key] = func(*args, **kwargs)
        return self._cache[cache_key]

    def cache_reset(self, key: str = None, *, is_match=True, is_safe=False):
        """
        Сброс кэша
        :param key: Ключ конкретного кэша, который требуется сбросить. Если None, то сбрасывается весь кэш.
        :param is_match: Сброс по точному совпадению ключа
        :param is_safe: если ключа в кэше не существует, то ошибки поднята не будет
        :return:
        """
        if key is None:
            self._cache = {}
        else:
            if is_match:
                if key not in self._cache:
                    if not is_safe:
                        raise ValueError(f"Cache key '{key}' was not found in class {self.__class__.__name__}")
                else:
                    del self._cache[key]
            else:
                keys = tuple(filter(lambda i: key in i, self._cache.keys()))
                if len(keys) == 0:
                    if not is_safe:
                        raise ValueError(f"Cache key match '{key}' was not found in the class {self.__class__.__name__}")
                else:
                    for _key in keys:
                        del self._cache[_key]
