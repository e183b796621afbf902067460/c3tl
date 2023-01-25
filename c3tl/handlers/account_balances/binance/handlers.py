from c3tl.interfaces.handlers.account_balances.interface import iAccountBalancesHandler

from c3f1nance.binance.Spot import BinanceSpotExchange
from c3f1nance.binance.USDTm import BinanceUSDTmExchange
from trad3r.typings.trader.typing import Trad3r

import time
import requests as r


class BinanceSpotAccountBalancesHandler(BinanceSpotExchange, iAccountBalancesHandler):

    def __init__(self, trader: Trad3r, *args, **kwargs) -> None:
        BinanceSpotExchange.__init__(self, *args, **kwargs)
        iAccountBalancesHandler.__init__(self, trader=trader)

    def _formatting(self, json_: dict) -> dict:
        return {
            'pit_qty': float(json_['free']) + float(json_['locked']),
            'pit_current_price': self.trader.get_price(first=json_['asset'])
        }

    def get_overview(
            self,
            ticker: str,
            *args, **kwargs
    ):
        overviews: list = list()
        account = self.account(timestamp=int(time.time() * 1000))
        if not self._validate_response(account):
            raise r.HTTPError(f'Invalid status code for account in {self.__class__.__name__}')
        account = account.json()
        for balance in account['balances']:
            if balance['asset'] == ticker:
                overviews.append(self._formatting(json_=balance))
                break
        return overviews


class BinanceUSDTmAccountBalancesHandler(BinanceUSDTmExchange, iAccountBalancesHandler):

    def __init__(self, trader: Trad3r, *args, **kwargs) -> None:
        BinanceUSDTmExchange.__init__(self, *args, **kwargs)
        iAccountBalancesHandler.__init__(self, trader=trader)

    def _formatting(self, json_: dict) -> dict:
        return {
            'pit_qty': float(json_['marginBalance']),
            'pit_current_price': self.trader.get_price(first=json_['asset'])
        }

    def get_overview(
            self,
            ticker: str,
            *args, **kwargs
    ):
        overviews: list = list()
        account = self.account(timestamp=int(time.time() * 1000))
        if not self._validate_response(account):
            raise r.HTTPError(f'Invalid status code for account in {self.__class__.__name__}')
        account = account.json()

        for asset in account['assets']:
            if asset['asset'] == ticker:
                overviews.append(self._formatting(json_=asset))
                break
        return overviews
