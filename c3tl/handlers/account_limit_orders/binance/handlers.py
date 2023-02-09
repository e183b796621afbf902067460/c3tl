from c3tl.interfaces.handlers.account_limit_orders.interface import iAccountLimitOrdersHandler

from c3f1nance.binance.USDTm import BinanceUSDTmExchange
from trad3r.typings.trader.typing import Trad3r

import time
import requests as r


class BinanceUSDTmAccountLimitOrdersHandler(BinanceUSDTmExchange, iAccountLimitOrdersHandler):

    def __init__(self, trader: Trad3r, *args, **kwargs) -> None:
        BinanceUSDTmExchange.__init__(self, *args, **kwargs)
        iAccountLimitOrdersHandler.__init__(self, trader=trader)

    def _formatting(self, json_: dict, ticker: str) -> dict:
        return {
            'limit_order_price': float(json_['price']),
            'current_price': self.trader.get_price(first=ticker[:-4], source='binance_usdt_m'),
            'qty': float(json_['origQty']),
            'side': json_['side']
        }

    def get_overview(
            self,
            ticker: str,
            *args, **kwargs
    ):
        overviews: list = list()
        open_orders = self.openOrders(symbol=ticker, timestamp=int(time.time() * 1000))
        if not self._validate_response(open_orders):
            raise r.HTTPError(f'Invalid status code for openOrders in {self.__class__.__name__}')
        open_orders = open_orders.json()
        for open_order in open_orders:
            overviews.append(self._formatting(json_=open_order, ticker=ticker))
        if not overviews:
            overviews.append(
                {
                    'limit_order_price': None,
                    'current_price': self.trader.get_price(first=ticker[:-4], source='binance_usdt_m'),
                    'qty': None,
                    'side': None
                }
            )
        return overviews
