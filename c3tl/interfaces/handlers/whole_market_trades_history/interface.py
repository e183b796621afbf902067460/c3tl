from abc import abstractmethod, ABC
import datetime


class iWholeMarketTradesHistoryHandler(ABC):

    @abstractmethod
    def get_overview(self, ticker: str, start: datetime.datetime, end: datetime.datetime, *args, **kwargs):
        raise NotImplementedError(f"{self.__class__.__name__} doesn't have an {self.get_overview.__name__}() implementation")
