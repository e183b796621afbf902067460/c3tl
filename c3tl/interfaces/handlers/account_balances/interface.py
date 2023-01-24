from abc import abstractmethod, ABC
from trad3er.typings.trader.typing import Trad3r


class iAccountBalancesHandler(ABC):

    def __init__(self, trader: Trad3r, *args, **kwargs) -> None:
        self._trader = trader

    @property
    def trader(self):
        return self._trader

    @abstractmethod
    def get_overview(self, ticker: str, *args, **kwargs):
        raise NotImplementedError(f"{self.__class__.__name__} doesn't have an {self.get_overview.__name__}() implementation")
