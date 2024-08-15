import logging
from typing import Any, Dict

from rich.console import Console
from rich.logging import RichHandler


class SingletonMeta(type):
    """싱글톤 메타 클래스"""

    _instances: Dict[type, Any] = {}

    def __call__(cls, *args: Any, **kwargs: Any) -> Any:
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class RichLogger(metaclass=SingletonMeta):

    def __init__(self):
        self.console = Console()
        self.logger = logging.getLogger("RichLogger")
        self.logger.setLevel(logging.DEBUG)
        handler = RichHandler()
        handler.setLevel(logging.DEBUG)
        self.logger.addHandler(handler)

    def debug(self, message: str) -> None:
        self.logger.debug(message)

    def info(self, message: str) -> None:
        self.logger.info(message)

    def warning(self, message: str) -> None:
        self.logger.warning(message)

    def error(self, message: str) -> None:
        self.logger.error(message)

    def critical(self, message: str) -> None:
        self.logger.critical(message)


logger = RichLogger()
console = Console()
