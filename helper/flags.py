from enum import IntEnum
from doctest import testmod


class Param(IntEnum):
    PARAM_BITS = 1
    PARAM_BYTES = 2


class Condition(IntEnum):
    ANY = 1
    ALL = 2


class Flags:
    """
    Класс работы с битовыми флагами.

    >>> f = Flags(0, Param.PARAM_BITS)
    Traceback (most recent call last):
        ...
    TypeError: Неправильное значение. Количество битов должно быть целым положительным числом.
    >>> f = Flags(10, 0)
    Traceback (most recent call last):
        ...
    TypeError: Неправильное значение. Значение должно быть Param.PARAM_BYTE(1) или Param.PARAM_BYTES(2).
    >>> f = Flags(2, Param.PARAM_BYTES)
    >>> f.number_of_bits
    16
    """

    # PARAM_BITS, PARAM_BYTES = (1, 2)
    # ANY, ALL = (1, 2)

    def __init__(self, number: int = 1, param: Param = Param.PARAM_BITS,
                 bit_mask: str | list[int] | tuple[int, ...] | set | int | None = None):
        """
        Инициализирует флаги битов. Если "bit_mask" не определен, то флаги остаются нулевый.

        >>> f = Flags(1, Param.PARAM_BYTES, '11000011')
        >>> f.str_bits
        '11000011'
        >>>

        :param number: Количество битов или байтов, в зависимости от значения параметра "param".
        :param param: Если PARAM_BITS, то будет создано указанное количество бит,
                    если PARAM_BYTES, то будет создано бит в соответствии с указанным количеством байт.
        :param bit_mask: Битовая маска указанная в виде строки битов, последовательности порядковых чисел,
                        или целого неотрицательного числа.
        """
        if not (isinstance(number, int) and number > 0):
            raise TypeError("Неправильное значение. Количество {0} должно быть целым положительным числом.".
                            format("битов" if param == Param.PARAM_BITS else "байтов"))
        if param not in (1, 2):
            raise TypeError("Неправильное значение. Значение должно быть Param.PARAM_BYTE(1) или Param.PARAM_BYTES(2).")
        # Если передали байты,
        if param == 2:
            # то подсчитаем, сколько это бит.
            bits = number * 8
        else:
            # Иначе запомним сколько передали именно в битах
            bits = number
        # Запомним сколько битов используется
        self.__number_of_bits = bits
        # Далее сформируем нулевой список рабочих бит
        self.__bits = 0
        """@param _list_bits: список рабочих битов
           @type _list_bits: list """
        # Если была сразу передана битовая маска,
        if bit_mask is not None:
            # то преобразуем переданную битовую маску для проверки,
            bit_mask = self.__convert_bit_mask(bit_mask)
            # и произведем установку бит по битовой маске.
            self.__bits |= bit_mask

    @property
    def value(self):
        """
        Возвращает состояние битовой маски в виде целого числа.

        >>> f = Flags(4, Param.PARAM_BITS)
        >>> f.value
        0
        >>> f.value = 15
        >>> f.value
        15
        >>> f.str_bits
        '1111'
        """
        return self.int_bits

    @value.setter
    def value(self, bit_mask: str | list[int] | tuple | set | int):
        """
        Устанавливает состояние битовой маски.
        :param bit_mask: Битовая маска представленная в виде строки, списка целых чисел, кортежа,
        множества или целого числа.
        :return:
        """
        # Для начала сбросим все биты в ноль.
        self.__bits = 0
        if bit_mask is not None:
            # Далее преобразуем переданную битовую маску для проверки,
            bit_mask = self.__convert_bit_mask(bit_mask)
            # и произведем установку бит по битовой маске.
            self.__bits |= bit_mask

    @property
    def number_of_bits(self):
        """
        Возвращает количество используемых бит.
        :return:
        """
        return self.__number_of_bits

    def __get_all_bits(self):
        """
        Возвращает биты со всеми установленными флагами.
        :return:
        """
        all_bits = 0
        for num in range(0, self.number_of_bits):
            all_bits |= 1 << num
        return all_bits

    @property
    def bin_bits(self) -> bin:
        """
        Возвращает битовую последовательность в виде значения bin.
        :return:
        """
        return bin(self.__bits)

    @property
    def int_bits(self) -> int:
        """
        Возвращает битовую последовательность в виде целого числа.
        :return:
        """
        return self.__bits

    @property
    def str_bits(self) -> str:
        """
        Возвращает битовую последовательность в виде строки.
        :return:
        """
        return self.__get_to_str()

    def __get_to_str(self) -> str:
        """
        Возвращает битовую последовательность в виде строки.
        :return:
        """
        str_bits = ""
        for bit in range(0, self.__number_of_bits):
            str_bits += "1" if (self.__bits & (1 << bit)) else "0"
        return str_bits

    def get_bit(self, num: int):
        """
        Возвращает состояние указанного бита.

        >>> f = Flags(1, Param.PARAM_BYTES)
        >>> f.set_bits((2,4,5,6), 1)
        >>> f.str_bits
        '01011100'
        >>> f.get_bit(2)
        1
        >>> f.get_bit(3)
        0
        >>>

        :param num: Порядковый номер бита, который надо вернуть.
        :return: Один или ноль.
        :raises TypeError: Проверяемый бит должен быть указан как неотрицательный порядковый
                            номер бита в битовой последовательности.
        """
        if not self.__validate_not_negative_int(num):
            raise TypeError("Проверяемый бит должен быть указан как неотрицательный порядковый "
                            "номер бита в битовой последовательности.")
        if num == 0:
            return 0
        return 1 if self.__bits & 1 << num - 1 != 0 else 0

    def get_bit_bool(self, num) -> bool:
        """
        Возвращает состояние указанного бита в виде логического значения.

        >>> f = Flags(1, Param.PARAM_BYTES)
        >>> f.set_bits((2,4,5,6), 1)
        >>> f.str_bits
        '01011100'
        >>> f.get_bit_bool(2)
        True
        >>> f.get_bit_bool(3)
        False
        >>>

        :param num: Порядковый номер бита, который надо вернуть.
        :return:
        :raises TypeError: Проверяемый бит должен быть указан как неотрицательный порядковый
                            номер бита в битовой последовательности.
        """
        return True if self.get_bit(num) == 1 else False

    def set_bit(self, num_bit: int, val: bool | int):
        """
        Устанавливает указанный бит.

        >>> f = Flags(1, Param.PARAM_BYTES)
        >>> f.str_bits
        '00000000'
        >>> f.set_bit(3, 1)
        >>> f.str_bits
        '00100000'
        >>> f.set_bit(2, 2)
        Traceback (most recent call last):
            ...
        TypeError: Значение может быть только логическое, либо 1 или 0.

        :param num_bit: Порядковый номер бита в битовой последоваетельнсоти, который нужно
                        перевести в состояние указанное в аргументе val.
        :param val:  Лгическое значение или 1 или 0, в которое надо перевести указанный бит.
        :return:
        :raises TypeError: Изменяемый бит должен быть указан как порядковый номер бита
                          больше нуля в битовой последовательности.
        """
        if not self.__validate_not_negative_int(num_bit):
            raise TypeError("Изменяемый бит должен быть указан как неотрицательный порядковый "
                            "номер бита в битовой последовательности.")

        # Если передали 0, то ничего делать не надо.
        if num_bit == 0:
            return

        bit_mask = 1 << num_bit - 1
        self.set_bits(bit_mask, val)

    def set_bits(self, bit_mask: str | list[int] | tuple[int, ...] | set | int, val: bool | int):
        """
        Устанавливает биты в соответствии битовой маске,
        в состояние указанное аргументом val.

        >>> f = Flags(1, Param.PARAM_BYTES)
        >>> f.str_bits
        '00000000'
        >>> f.set_bits("1001001", True)
        >>> f.str_bits
        '10010010'
        >>> f = Flags(1, Param.PARAM_BYTES)
        >>> f.str_bits
        '00000000'
        >>> f.set_bits("1001001", True)
        >>> f.str_bits
        '10010010'

        :param bit_mask: Битовая маска указанная в виде строки битов, последовательности порядковых чисел,
                        или целовго неотрицательного числа.
        :param val: Логическое значение или 1 или 0, в которое надо установить указанные в битовой маске биты.
        :raisea TypeError: Битовая маска не может быть отрицательной. |
                          Недопустимый тип битовой маски.
        """
        # Для начала преобразуем переданную битовую маску для проверки.
        bit_mask = self.__convert_bit_mask(bit_mask)

        if self.__convert_val_to_bool(val):
            # Произведем установку бит по битовой маске.
            self.__bits |= bit_mask
        else:
            # Или же произведем сброс по битовой маске.
            self.__bits &= ~bit_mask

    def check_bit(self, num_bit: int, val: bool|int) -> bool | None :
        """
        Проверяет битовый массив значений на соответствие переданному порядковому номеру бита.

        >>> f = Flags(1, Param.PARAM_BYTES)
        >>> f.set_bits((2,4,5,6), 1)
        >>> f.str_bits
        '01011100'
        >>> f.check_bit(1, 1)
        False
        >>> f.check_bit(1, 0)
        True
        >>> f.check_bit(2, 1)
        True
        >>> f.check_bit(2, 0)
        False
        >>>

        :param num_bit: Порядковый номер бита в битовой последоваетельнсоти, который нужно
                       проверить на состояние указанное в аргументе val.
        :param val: Логическое значение или 1 или 0, на которое надо проверить указанный бит.
        :return:
        :raises TypeError: Проверямый бит должен быть указан как порядковый номер бита
                          больше нуля в битовой последовательности.
        """
        if not self.__validate_not_negative_int(num_bit):
            raise TypeError("Изменяемый бит должен быть указан как неотрицательный порядковый "
                            "номер бита в битовой последовательности.")

        # Если передали 0, то ничего делать не надо.
        if num_bit == 0:
            return None

        bit_mask = (num_bit,)
        return self.check_bits(bit_mask, val)

    def check_bits(self, bit_mask: str | list[int] | tuple[int, ...] | set | int, val: bool | int, condition: Condition = Condition.ALL):
        """
        Проверяет битовый массив значений на соответствие битовой строке
        или массиву порядковых номеров битов.

        >>> f = Flags(1, Param.PARAM_BYTES)
        >>> f.set_bits((2,4,5,6), 1)
        >>> f.str_bits
        '01011100'
        >>> f.check_bits('01011100', 1, Condition.ALL)
        True
        >>> f.check_bits('00011100', 1, Condition.ALL)
        True
        >>> f.check_bits('11011100', 1, Condition.ALL)
        False
        >>> f.check_bits('00000100', 1, Condition.ANY)
        True
        >>>

        :param bit_mask: Битовая маска указанная в виде строки битов,
                        последовательности порядковых чисел, или целого неотрицательного числа.
        :param val: Логическое значение или 1 или 0, на которое надо проверить указанные в битовой маске биты.
        :param condition: Условие проверки, все биты, или любый из битов.
        :return:
        :raises TypeError: Условие может быть только Condition.ANY (1) или Condition.ALL (2).
        """
        if condition not in (Condition.ALL, Condition.ANY):
            raise TypeError("Условие может быть только Condition.ANY (1) или Condition.ALL (2).")

        # Для начала преобразуем переданную битовую маску для проверки.
        bit_mask = self.__convert_bit_mask(bit_mask)

        # Если надо проверить биты на установку,
        if self.__convert_val_to_bool(val):
            # то их можно проверить на любой из установленых битов,
            if condition == Condition.ANY:
                return self.__bits & bit_mask != 0
            else:
                # или на то, чтобы бы все проверяемые биты были установлены.
                return self.__bits & bit_mask == bit_mask
        # Иначе проверить биты на сброс. Для этого нам надо бует инверсировать битовый массив значений
        else:
            # Их так же можно проверить на любой из сброшенных битов,
            if condition == Condition.ANY:
                return ~self.__bits & bit_mask != 0
            else:
                # или на то, чтобы бы все проверяемые биты были сброшены.
                return ~self.__bits & bit_mask == bit_mask

    def inverse_bit(self, num_bit: int):
        """
        Переключает указанный бит в противоположенное значение.

        >>> f = Flags(1, Param.PARAM_BYTES)
        >>> f.set_bits((2,4,5,6), 1)
        >>> f.str_bits
        '01011100'
        >>> f.inverse_bit(6)
        >>> f.str_bits
        '01011000'
        >>>

        :param num_bit: Порядковый номер бита в битовой последоваетельнсоти, который нужно
                       переключить в противоположенное состояние.
        """
        if not self.__validate_not_negative_int(num_bit):
            raise TypeError("Переключаемый бит должен быть указан как неотрицательный порядковый "
                            "номер бита в битовой последовательности.")

        # Если передали 0, то ничего делать не надо.
        if num_bit == 0:
            return

        bit_mask = (num_bit,)
        self.inverse_bits(bit_mask)

    def inverse_bits(self, bit_mask: str | list[int] | tuple[int, ...] | set | int):
        """
        Переключает биты указанные в битовой маске в противоположенное значение.

        >>> f = Flags(1, Param.PARAM_BYTES)
        >>> f.set_bits((2,4,5,6), 1)
        >>> f.str_bits
        '01011100'
        >>> f.inverse_bits('11110000')
        >>> f.str_bits
        '10101100'
        >>>

        :param bit_mask: Битовая маска указанная в виде строки битов, последовательности порядковых чисел,
                        или целого неотрицательного числа.
        """
        # Для начала преобразуем переданную битовую маску для инверсии.
        bit_mask = self.__convert_bit_mask(bit_mask)
        self.__bits ^= bit_mask

    def __convert_bit_mask(self, bit_mask: str | list[int] | tuple[int, ...] | set | int):
        """
        Конвертирует битовую маску в зависимости от того, в каком виде она была передана.
        :param bit_mask: Битовая маска.
        :return:
        :raises TypeError: Битовая маска не может быть отрицательной. |
                            Недопустимый тип битовой маски.
        """
        # Для начала преобразуем переданную битовую маску для проверки.
        if isinstance(bit_mask, str):
            bit_mask = self.util_convert_str_to_bit_mask(bit_mask)
        elif isinstance(bit_mask, (list, tuple, set)):
            bit_mask = self.util_convert_list_num_to_bit_mask(bit_mask)
        elif isinstance(bit_mask, int):
            if bit_mask < 0:
                raise TypeError("Битовая маска не может быть отрицательной.")
        else:
            raise TypeError("Недопустимый тип битовой маски.")
        return bit_mask

    @staticmethod
    def util_convert_str_to_bit_mask(str_: str):
        """
        Статический метод преобразует битовую строку в битовую маску.

        >>> num = Flags.util_convert_str_to_bit_mask("10110011")
        >>> num
        205
        >>> Flags.util_int_to_bitstring(num)
        '10110011'
        >>>
        :param str_: Битовая строка типа: "10110011".
        :return:
        :raises TypeError: Биты могут иметь значения только 1 или 0.
        """
        list_num = []
        i = 1
        for char in str_:
            if char == '1':
                list_num.append(i)
            elif char != '0':
                raise TypeError("Биты могут иметь значения только 1 или 0.")
            i += 1
        return Flags.util_convert_list_num_to_bit_mask(list_num)

    @staticmethod
    def util_convert_list_num_to_bit_mask(list_num: list[int] | tuple[int, ...]):
        """
        Статический метод преобразует список порядковых чисел в битовую маску.

        >>> lst = (1, 4, 6, 7, 8)
        >>> num = Flags.util_convert_list_num_to_bit_mask(lst)
        >>> Flags.util_int_to_bitstring(num)
        '10010111'
        >>>

        :param list_num: Список порядковых чисел.
        :return:
        """
        num_bit = 0

        # Пробежимся по всему списку
        for num in list_num:
            # и установим каждый бит по указанному порядковому номеру
            num_bit |= 1 << num - 1
        return num_bit

    @classmethod
    def util_int_to_bitstring(cls, val: int):
        """
        Статический метод отображает числа в виде строки битов.

        >>> Flags.util_int_to_bitstring(7)
        '111'
        >>> Flags.util_int_to_bitstring(8)
        '0001'

        :param val: Целое неотрицательное число, которое надо преобразовать в строку битов.
        :return: Строка битов.
        :raises TypeError: Значение должно быть целым неотрицательным числом.
        """
        # Для начала проверим, что было передано неотрицательное целое число.
        if not cls.__validate_not_negative_int(val):
            raise TypeError("Значение должно быть целым неотрицательным числом.")
        # Если передали ноль,
        if val == 0:
            # то и вернем ноль.
            return "0"
        num = 0
        str_bits = ""
        # Иначе будем проходить до тех пор, пока не найдем сколько бит потребуется
        # для формирования переданного числа.
        while True:
            if val < (1 << num):
                break
            num += 1
        # Теперь пройдемся по каждому биту,
        for bit in range(0, num):
            # и если этот бит в числе установлен, то укажим его как 1, иначе 0
            str_bits += "1" if (val & (1 << bit)) else "0"
        return str_bits

    @staticmethod
    def __convert_val_to_bool(val: bool | int):
        """
        Преобразует 1 и 0 в логический тип, или возвращает значение,
        если переданное значение уже логическое.

        :param val:
        :return:
        :raises TypeError: Значение может быть только логическое, либо 1 или 0.
        """
        if isinstance(val, bool):
            return val
        elif val in (0, 1):
            return True if val == 1 else False
        else:
            raise TypeError("Значение может быть только логическое, либо 1 или 0.")

    @staticmethod
    def __validate_not_negative_int(num: int) -> bool:
        """
        Проверяет значение на целое неотрицательное число.
        :param num:
        :return:
        """
        return False if (not isinstance(num, int) or num < 0) else True

    def __str__(self):
        return self.__get_to_str()

    def __int__(self):
        return self.__bits

    def __repr__(self):
        return f"Flags({self.number_of_bits}, {Param.PARAM_BITS}, '{self.str_bits}')"

    def __eq__(self, other):
        """
        Равно.

        @param other:
        @type other: Flags
        @return:
        """
        return self.__bits == other.__bits

    def __lt__(self, other):
        """
        Меньше.

        @param other:
        @type other: Flags
        @return:
        """
        return self.__bits < other.__bits

    def __le__(self, other):
        """
        Меньше либо равно.

        @param other:
        @type other: Flags
        @return:
        """
        return self.__bits <= other.__bits

    def __and__(self, other):
        """
        Битовый и логический оператор И (&).

        @param other:
        @type other: Flags
        @return:
        """
        return Flags(self.number_of_bits, Param.PARAM_BITS, self.__bits & other.__bits)

    def __iand__(self, other):
        """
        Битовый и логический оператор присваивания И (&=).

        @param other:
        @type other: Flags
        @return:
        """
        self.__bits &= other.__bits
        return self

    def __or__(self, other):
        """
        Битовый и логический оператор ИЛИ (|).

        @param other:
        @type other: Flags
        @return:
        """
        return Flags(self.number_of_bits, Param.PARAM_BITS, self.__bits | other.__bits)

    def __ior__(self, other):
        """
        Битовый и логический оператор присваивания И(|=).

        @param other:
        @type other: Flags
        @return:
        """
        self.__bits |= other.__bits
        return self

    def __xor__(self, other):
        """
        Битовый и логический оператор исключающее ИЛИ (^).

        @param other:
        @type other: Flags
        @return:
        """
        return Flags(self.number_of_bits, Param.PARAM_BITS, self.__bits ^ other.__bits)

    def __ixor__(self, other):
        """
        Битовый и логический оператор исключающее ИЛИ (^=).

        @param other:
        @type other: Flags
        @return:
        """
        self.__bits ^= other.__bits
        return self

    def __invert__(self):
        """
        Битовый и логический оператор НЕТ (~).

        @return:
        """
        return Flags(self.number_of_bits, Param.PARAM_BITS, self.__bits ^ self.__get_all_bits())

    def __add__(self, other):
        """
        Арифметическая операция +.

        @param other:
        @type other: Flags
        @return:
        """
        return Flags(self.number_of_bits, Param.PARAM_BITS, self.__bits | other.__bits)

    def __iadd__(self, other):
        """
        Арифметическая операция +=.

        @param other:
        @type other: Flags
        @return:
        """
        self.__bits |= other.__bits
        return self

    def __sub__(self, other):
        """
        Арифметическая операция -.

        @param other:
        @type other: Flags
        @return:
        """
        return Flags(self.number_of_bits, Param.PARAM_BITS, self.__bits ^ other.__bits)

    def __isub__(self, other):
        """
        Арифметическая операция -=.

        @param other:
        @type other: Flags
        @return:
        """
        self.__bits ^= other.__bits
        return self

    def __neg__(self):
        """
       Арифметическая операция отрицания (-x).

        @return:
        """
        return Flags(self.number_of_bits, Param.PARAM_BITS, self.__bits ^ self.__get_all_bits())

    def __hash__(self):
        return hash(self.__bits)

    def __len__(self):
        return self.__number_of_bits

    def __bytes__(self):
        return bytes(self.__bits)


if __name__ == "__main__":
    testmod(name='Flags', verbose=True)
