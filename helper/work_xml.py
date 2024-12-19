from xml.etree import ElementTree
from xml.etree.ElementTree import Element


def xml_converter_to_lofl(_xml: Element | str):
    """ Преобразуете XML в список списков. """
    _el = _xml if isinstance(_xml, Element) else ElementTree.fromstring(_xml)
    # Первый элемент списка - наименование тэга
    xml_element_list = [_el.tag]
    # Второй элемент списка - отсортированный список кортежей аттрибутов.
    attrs = sorted(_el.items())

    # Третий список - отсортированный список преобразованных в список-списков XML-под элементов.
    sub_el = sorted([xml_converter_to_lofl(el) for el in _el.iterfind('./')])
    # Если в XML присутствует текст, то он добавляется в третий список в начальную позицию.
    if (text := _el.text) is not None:
        if len(text := text.strip()) > 0:
            sub_el = [text] + sub_el
    xml_element_list += [attrs, sub_el]
    return xml_element_list


def compare_xml(str_xml_1: Element | str, str_xml_2: Element | str, str_xpath: str = None):
    """
    Проверяет вхождения str_xml_1 в str_xml_2.
    :param str_xml_1: XML который проверятся.
    :param str_xml_2: XML с которым сверяется.
    :param str_xpath: Строка xpath для выбирания нужных узлов из XML.
    :return:
    """
    def get_hash(str_xml, _str_xpath):
        """
        Возвращает однозначный HASH строки XML.
        :param str_xml: Строка XML.
        :param _str_xpath: Строка xpath для выбирания нужных узлов из XML.
        :return: Список HASH-сумм переданного XML.
        """
        _xml: Element = ElementTree.fromstring(str_xml) if isinstance(str_xml, str) else str_xml
        # Производится поиск указанных в XPATH узлов.
        xml_list = _xml.findall(_str_xpath)
        # Формируется список строк найденных узлов преобразованных в список списков.
        xml_str_lofl = [xml_converter_to_lofl(item) for item in xml_list]
        # logger.debug(f"XML string with XPATH '{_str_xpath}': {xml_str_lofl}")
        # Текстовые строки списка списков преобразуются в HASH-и.
        return list(map(lambda i: hash(repr(i)), xml_str_lofl))

    # Если xpath не указан, то сравнивается весь XML.
    if str_xpath is None:
        xml_1_lofl = xml_converter_to_lofl(str_xml_1)
        hash_xml_str_1 = hash(repr(xml_1_lofl))

        xml_2_lofl = xml_converter_to_lofl(str_xml_2)
        hash_xml_str_2 = hash(repr(xml_2_lofl))
        return hash_xml_str_1 == hash_xml_str_2
    else:
        xml_hash_list_1 = get_hash(str_xml_1, str_xpath)
        xml_hash_list_2 = get_hash(str_xml_2, str_xpath)
        return all(map(lambda i: any(map(lambda j: j == i, xml_hash_list_2)),  xml_hash_list_1))


def convert_response_to_string(response: str | Element, is_formatted: bool = False):
    """
    Конвертирует XML-ответ в строку.
    :param response: Отвёт в формате JSON или строки.
    :param is_formatted: Должен ли ответ быть отформатирован.
    :return:
    """
    if not(isinstance(response, str) or isinstance(response, Element)):
        raise ValueError("The response must be in string or XML format")
    # Если ответ должен быть отформатирован,
    if is_formatted:
        # то вначале строковый вариант ответа надо преобразовать в XML,
        # только его потом можно отформатировать.
        response = ElementTree.fromstring(response) if isinstance(response, str) else response
        ElementTree.indent(response, space="  ", level=0)
    return response if isinstance(response, str) else ElementTree.tostring(response).decode()