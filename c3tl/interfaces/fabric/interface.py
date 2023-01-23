from abc import ABC, abstractmethod


class iFabric(ABC):

    def __init__(self) -> None:
        self._handlers: dict = dict()

    @abstractmethod
    def add_handler(self, *args, **kwargs) -> None:
        raise NotImplementedError(f"{self.__class__.__name__} doesn't have an {self.add_handler.__name__}() implementation")

    @abstractmethod
    def get_handler(self, *args, **kwargs) -> object:
        raise NotImplementedError(f"{self.__class__.__name__} doesn't have a {self.get_handler.__name__}() implementation")
