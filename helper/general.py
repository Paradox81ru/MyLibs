import ctypes
from pathlib import Path


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
