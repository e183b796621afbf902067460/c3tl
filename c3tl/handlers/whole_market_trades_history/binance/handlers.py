from c3tl.interfaces.handlers.whole_market_trades_history.interface import iWholeMarketTradesHistoryHandler

from c3f1nance.binance.Spot import BinanceSpotExchange
from c3f1nance.binance.USDTm import BinanceUSDTmExchange

import datetime
import requests as r


class BinanceSpotWholeMarketTradesHandler(BinanceSpotExchange, iWholeMarketTradesHistoryHandler):

    @staticmethod
    def _formatting(json_: dict) -> dict:
        return {
            'pit_price': json_['p'],
            'pit_qty': json_['q'],
            'pit_ts': json_['T'],
            'pit_side': 'BUY' if json_['m'] else 'SELL'
        }

    def get_overview(
            self,
            ticker: str,
            start: datetime.datetime, end: datetime.datetime,
            *args, **kwargs
    ):
        overviews: list = list()
        end = int(end.timestamp()) * 1000

        agg_trades = self.aggTrades(
            symbol=ticker,
            startTime=int(start.timestamp()) * 1000,
            endTime=end,
            limit=1000
        )
        if not self._validate_response(agg_trades):
            raise r.HTTPError(f'Invalid status code for aggTrades in  {self.__class__.__name__}')
        agg_trades = agg_trades.json()
        overviews.extend([self._formatting(json_=agg_trade) for agg_trade in agg_trades])

        while True:
            start = agg_trades[-1]['T'] + 1

            agg_trades = self.aggTrades(
                symbol=ticker,
                startTime=start,
                endTime=end,
                limit=1000
            )
            if not self._validate_response(agg_trades):
                raise r.HTTPError(f'Invalid status code for aggTrades in  {self.__class__.__name__}')
            agg_trades = agg_trades.json()
            if not agg_trades:
                break
            overviews.extend([self._formatting(json_=agg_trade) for agg_trade in agg_trades])
        return overviews
