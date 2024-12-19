import os
import time
from pathlib import Path
from typing import final

from helper.general import RunFunction, repeat_attempts


def download_folder_path():
    """ Полное наименование директории загрузки файлов. """
    # return os.path.join(os.environ['USERPROFILE'], 'Downloads')
    return Path.home() / 'Downloads'


def last_file_from_download_folder(type_file: str = "") -> Path | None:
    """
    Возвращает последний файл по дате из директории загруженных файлов.
    :param type_file: Тип последнего файла. По умолчанию "", то есть все типы файлов.
    :return: Полное наименование последнего файла, если такой есть, или None.
    """
    # Берем из директории только файлы и преобразуем их в полные имена,
    _download_folder_path = download_folder_path()
    files = list(filter(
        lambda f: f.is_file(),
        [(_download_folder_path / file) for file in os.listdir(_download_folder_path)
         if file.endswith(type_file)]))
    try:
        # а далее возвращаем файл с самым большим временем создания
        return max(files, key=lambda f: f.stat().st_ctime) if len(files) > 0 else None
    except FileNotFoundError:
        return None


def check_download_last_file(type_file: str = None, timeout: float = 10) -> Path:
    """
    Проверяет последний скаченный файл в директории загрузки.
    :param type_file: Расширение файла, который проверяется. Если None, то проверяется только по дате создания.
    :param timeout: Время ожидания загрузки файла.
    :return: Полное Наименование последнего скачанного файла.
    :raises FileNotFoundError:
    """
    minutes = 5
    # Пять минут
    point_time: final = 60 * minutes

    def not_temp_downloading_file(file: Path):
        """ Проверяет, что файл не является временным файлом закачки """
        return all(map(lambda e: file.suffix != e, ('.part', '.tmp', '.crdownload', '.opdownload')))

    def condition_time(file: Path):
        """ Условие поиска пока не появится не пустой и не временный файл закачки, созданный не позднее чем 5 минут """
        return (file is not None and file.exists() and not_temp_downloading_file(file)
                and (time.time() - file.stat().st_ctime < point_time) and file.stat().st_size > 0)

    def condition_time_and_extension(file: Path):
        """ Условие поиска пока не появится ни пустой и ни временный файл закачки, созданный не позднее чем 5 минут
        и указанного типа. """
        return condition_time(file) and file.suffix == f".{type_file}"

    func = last_file_from_download_folder if type_file is None \
        else RunFunction(func=last_file_from_download_folder, args=[type_file])
    try:
        # Делаются попытки получить файл, пока не будет выполнено условие.
        filename = repeat_attempts(
            func,
            condition_time if type_file is None else condition_time_and_extension, timeout)
        return filename
    except TimeoutError:
        ext_add = f"with '{type_file}' extension " if type_file is not None else ""
        raise FileNotFoundError(f"File downloaded within {minutes} minutes "
                                f"{ext_add}were not detected")


def wait_file_remove(filename: Path, timeout):
    """
    Ожидание, пока файл не будет удалён
    :param filename:
    :param timeout:
    :return:
    :raises TimeoutError: истекло время ожидания удаления файла
    """
    repeat_attempts(lambda: filename.exists(), lambda r: not r, timeout)
