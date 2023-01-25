from c3tl.interfaces.handlers.account_liquidations.interface import iAccountLiquidationsHandler

from c3f1nance.binance.USDTm import BinanceUSDTmExchange
from trad3er.typings.trader.typing import Trad3r

import time
import requests as r


class BinanceUSDTmAccountLiquidationsHandler(BinanceUSDTmExchange, iAccountLiquidationsHandler):

    def __init__(self, trader: Trad3r, *args, **kwargs) -> None:
        BinanceUSDTmExchange.__init__(self, *args, **kwargs)
        iAccountLiquidationsHandler.__init__(self, trader=trader)

    def _formatting(self, json_: dict, ticker: str) -> dict:
        return {
            'pit_amt': float(json_['positionAmt']),
            'pit_entry_price': float(json_['entryPrice']),
            'pit_liquidation_price': float(json_['liquidationPrice']),
            'pit_current_price': self.trader.get_price(first=ticker[:-4], source='binance_usdt_m'),
            'pit_side': json_['positionSide'],
            'pit_leverage': float(json_['leverage']),
            'pit_un_pnl': float(json_['unRealizedProfit'])
        }

    def get_overview(
            self,
            ticker: str,
            *args, **kwargs
    ):
        overviews: list = list()
        position_risk = self.positionRisk(symbol=ticker, timestamp=int(time.time() * 1000))
        if not self._validate_response(position_risk):
            raise r.HTTPError(f'Invalid status code for positionRisk in {self.__class__.__name__}')
        position_risk = position_risk.json()
        for position in position_risk:
            overviews.append(self._formatting(json_=position, ticker=ticker))
        return overviews
