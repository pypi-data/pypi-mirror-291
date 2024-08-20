import configparser
import json
import toml
import yaml

from pathlib import Path
from typing import Any


type DeleteOptions = str | list | tuple
type FetchOptions = list | tuple
type FetchResponse = dict[str, Any] | list[dict[str, Any]]
type Nothing = None


def exists_check(method):
    def wrapper(self, *args, **kwargs):
        if self.use_exists_check:
            if not self.cfg_path.exists():
                raise FileNotFoundError(f'{self.cfg_path} does not exist')
        return method(self, *args, **kwargs)
    return wrapper


class BaseConfig:
    """Базовый класс для работы с конфигурационными файлами.

    Args:
        cfg_path (Path | str): Путь к конфигурационному файлу.
        use_exists_check (bool, optional): Флаг, указывающий на 
        необходимость проверки существования файла. По умолчанию True.

    Attributes:
        cfg_path (Path): Разрешенный путь к конфигурационному файлу.
        use_exists_check (bool): Флаг, указывающий на необходимость 
        проверки существования файла.
        extension (str): Расширение конфигурационного файла.
    """

    def __init__(self, cfg_path: Path | str, use_exists_check: bool = True):
        self.cfg_path = Path(cfg_path).resolve()
        self.use_exists_check = use_exists_check
        self.extension = self.cfg_path.suffix

    def __str__(self) -> str:
        return f'{self.__class__.__name__}\n{self.__class__.__doc__}'

    @property
    def activate(self):
        """Возвращает экземпляр класса, соответствующего расширению 
        конфигурационного файла.

        Raises:
            TypeError: Если расширение файла не поддерживается.

        Returns:
            object: Экземпляр класса, соответствующего расширению 
            конфигурационного файла.
        """
        match self.extension:
            case '.toml' | '.json' | '.yaml' | '.cfg':
                return UniversalConfigFile(self.cfg_path, self.use_exists_check)
            case '.ini':
                return INIConfigFile(self.cfg_path, self.use_exists_check)
            case _:
                raise TypeError(f'{self.extension} is not supported')


class UniversalConfigFile(BaseConfig):
    """
    Класс UniversalConfigFile является специализированным классом 
    BaseConfig, предназначенным для работы с различными типами 
    конфигурационных файлов.

    Args:
        BaseConfig (_type_): Базовый класс, от которого наследуется 
        UniversalConfigFile.
    """

    def __init__(self, cfg_path: Path | str, use_exists_check: bool = True):
        """
        Инициализирует экземпляр класса UniversalConfigFile.

        Args:
            cfg_path (Path | str): Путь к конфигурационному файлу.
            use_exists_check (bool, optional): Флаг, указывающий, 
            следует ли выполнять проверку существования файла. 
            По умолчанию True.
        """
        super().__init__(cfg_path, use_exists_check)

    def exists(self) -> bool:
        """
        Проверяет, существует ли конфигурационный файл.

        Returns:
            bool: Возвращает True, если файл существует, 
            и False в противном случае.
        """
        return self.cfg_path.exists()

    @exists_check
    def fetch(self, section: FetchOptions | None = None) -> FetchResponse:
        """
        Загружает конфигурацию из файла.

        Args:
            section (FetchOptions | None, optional): Ограничение по 
            секциям для загрузки. По умолчанию None.

        Raises:
            TypeError: Если section не является списком, 
            кортежом или None. По умолчанию None.

        Returns:
            FetchResponse: Возвращает загруженную конфигурацию.
        """
        if not isinstance(section, (list, tuple)) and section is not None:
            raise TypeError(f'section must be list or tuple, not {type(section)}')

        with open(self.cfg_path, 'r', encoding='utf-8') as file:
            config = self.__loader(file)
            return config if section is None else [config[k] for k in section]

    @exists_check
    def get(self, section: str) -> dict[str, Any]:
        """
        Получает конфигурацию из файла по указанной секции.

        Args:
            section (str): Название секции.

        Raises:
            TypeError: Если section не является строкой.

        Returns:
            dict[str, Any]: Возвращает конфигурацию секции.
        """
        if not isinstance(section, str):
            raise TypeError(f'section must be str, not {type(section)}')

        with open(self.cfg_path, 'r', encoding='utf-8') as file:
            config = self.__loader(file)
            return config[section]

    @exists_check
    def set(self, section: str, request: dict[str, Any]) -> Nothing:
        """
        Обновляет конфигурацию в файле по указанной секции.

        Args:
            section (str): Название секции.
            request (dict[str, Any]): Обновляемые данные.

        Raises:
            TypeError: Если request не является словарем.

        Returns:
            Nothing: Возвращает None.
        """
        if not isinstance(request, dict):
            raise TypeError(f'request must be dict, not {type(request)}')

        with open(self.cfg_path, 'r', encoding='utf-8') as file:
            config = self.__loader(file)

            if section in config.keys():
                config[section].update(request)
            else: config[section] = request

        with open(self.cfg_path, 'w', encoding='utf-8') as file:
            self.__dumper(config, file)

    @exists_check
    def delete(self, section: DeleteOptions | None = None) -> Nothing:
        """
        Удаляет секцию или секции из конфигурационного файла.

        Args:
            section (DeleteOptions | None, optional): Ограничение по 
            секциям для удаления. По умолчанию None.

        Raises:
            TypeError: Если section не является строкой, 
            списком или кортежом.

        Returns:
            Nothing: Возвращает None.
        """
        if not isinstance(section, (str, list, tuple)) and section is not None:
            raise TypeError(f'section must be str, list or tuple, not {type(section)}')

        with open(self.cfg_path, 'r', encoding='utf-8') as file:
            config = self.__loader(file)

            if isinstance(section, str):
                del config[section]
            elif isinstance(section, (list, tuple)):
                for k in section: del config[k]
            else: config.clear()

        with open(self.cfg_path, 'w', encoding='utf-8') as file:
            self.__dumper(config, file)

    def __loader(self, file, /):
        """
        Загружает конфигурацию из файла в зависимости 
        от расширения файла.

        Args:
            file: Открытый для чтения файл.

        Returns:
            dict: Возвращает загруженную конфигурацию.
        """
        if self.extension == '.toml' or '.cfg':
            config = toml.load(file)
        elif self.extension == '.json':
            config = json.load(file)
        else: config = yaml.safe_load(file)

        return config

    def __dumper(self, config, file, /):
        """
        Сохраняет конфигурацию в файл в зависимости 
        от расширения файла.

        Args:
            config (dict): Конфигурация для сохранения.
            file: Открытый для записи файл.
        """
        if self.extension == '.toml' or '.cfg':
            toml.dump(config, file)
        elif self.extension == '.json':
            json.dump(config, file)
        else: yaml.safe_dump(config, file)


class INIConfigFile(BaseConfig):
    """
    Класс для работы с INI-файлами.

    Args:
        BaseConfig (_type_): Базовый класс конфигурационного файла.
    """

    def __init__(self, cfg_path: Path | str, use_exists_check: bool = True):
        """
        Инициализация объекта класса INIConfigFile.

        Args:
            cfg_path (Path | str): Путь к INI-файлу.
            use_exists_check (bool, optional): Флаг, указывающий на 
            необходимость проверки существования файла. 
            По умолчанию True.
        """
        super().__init__(cfg_path, use_exists_check)
        self.parser = configparser.ConfigParser()

    def exists(self) -> bool:
        """
        Проверка существования INI-файла.

        Returns:
            bool: Возвращает True, если файл существует, 
            и False в противном случае.
        """
        return self.cfg_path.exists()
