from typing import Generic

from c3tl.interfaces.fabric.interface import iFabric
from c3tl.typings.handlers.whole_market_trades_history.typing import WholeMarketTradesHistoryHandler

from c3tl.handlers.whole_market_trades_history.binance.handlers import BinanceSpotWholeMarketTradesHandler


class WholeMarketTradesHistoryFabric(iFabric):

    def add_handler(self, exchange: str, handler: Generic[WholeMarketTradesHistoryHandler]) -> None:
        if not self._handlers.get(exchange):
            self._handlers[exchange] = handler

    def get_handler(self, exchange: str) -> Generic[WholeMarketTradesHistoryHandler]:
        handler = self._handlers.get(exchange)
        if not handler:
            raise ValueError(f'Set Whole Market Trades History overview handler for {exchange}')
        return handler


wholeMarketTradesHistoryFabric = WholeMarketTradesHistoryFabric()

wholeMarketTradesHistoryFabric.add_handler(exchange='binance_spot', handler=BinanceSpotWholeMarketTradesHandler)