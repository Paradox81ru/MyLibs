def cached_reader(fn):
    """ Декоратор для кэшера. """
    def func(self, *args, **kwargs):
        def logger_debug(msg):
            if hasattr(self, '_BM'):
                self._BM.logger.debug(msg)

        cache_key = fn.__name__
        for arg in args:
            cache_key += f"_{arg}"
        for key, value in kwargs.items():
            cache_key += f"_{key}={value}"
        if cache_key not in self._cache:
            logger_debug(f"Writing data of the '{self.__class__.__name__}' class to the cache by key '{cache_key}'")
            self._cache[cache_key] = fn(self, *args, **kwargs)
        logger_debug(f"Reading data of the '{self.__class__.__name__}' class from the cache by key '{cache_key}'")
        return self._cache[cache_key]
    return func


class CachedReader:
    """ Класс кэшер. """
    def __init__(self, _logger=None):
        self._logger = _logger
        self._cache = {}

    def _logger_debug(self, msg):
        """ Добавляет Сообщение в дебаг логгера. """
        if self._logger is not None:
            self._logger.debug(msg)

    def _cached_reader(self, func: callable, *args, **kwargs):
        """ Читает значение переменной из кэша. """
        cache_key = func.__name__
        for arg in args:
            cache_key += f"_{arg}"
        for key, value in kwargs.items():
            cache_key += f"_{key}={value}"
        if cache_key not in self._cache:
            self._logger_debug(f"Writing data of the '{self.__class__.__name__}' class to the cache by key "
                               f"'{cache_key}'")
            self._cache[cache_key] = func(*args, **kwargs)
        self._logger_debug(f"Reading data of the '{self.__class__.__name__}' class from the cache by key '{cache_key}'")
        return self._cache[cache_key]

    def cache_reset(self, key: str = None, *, is_match=True):
        """
        Сброс кэша.
        :param key: Ключ конкретного кэша, который требуется сбросить. Если None, то сбрасывается весь кэш.
        :param is_match: Если True, то сброс по точному совпадению ключа. Иначе по вхождению в наименование ключа
        :return:
        """
        if key is None:
            self._logger_debug(f"Clearing the entire cache '{self.__class__.__name__}'")
            self._cache = {}
        else:
            if is_match:
                if key in self._cache:
                    self._logger_debug(f"Clearing the cache '{self.__class__.__name__}' by key {key}")
                    del self._cache[key]
            else:
                keys = tuple(filter(lambda i: key in i, self._cache.keys()))
                for _key in keys:
                    self._logger_debug(f"Clearing the cache '{self.__class__.__name__}' by key {_key} "
                                       f"coincidentally {key}")
                    del self._cache[_key]

            if key in self._cache:
                self._logger_debug(f"Clearing the cache '{self.__class__.__name__}' by key {key}")
                del self._cache[key]