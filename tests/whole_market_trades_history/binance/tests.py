import unittest

import builtins
from datetime import datetime, timezone, timedelta

from c3tl.handlers.whole_market_trades_history.binance.handlers import BinanceSpotWholeMarketTradesHandler
from c3tl.abstract.fabric import c3Abstract
from c3tl.bridge.configurator import C3BridgeConfigurator


class TestBinanceSpotWholeMarketTradesHandler(unittest.TestCase):

    product = C3BridgeConfigurator(
        abstract=c3Abstract,
        fabric_name='whole_market_trades_history',
        handler_name='binance_spot'
    ).produce_handler()
    handler = product()

    def testInstance(self):
        self.assertIsInstance(self.handler, BinanceSpotWholeMarketTradesHandler)

    def test_get_overview(self):
        end_time = datetime.utcnow()
        start_time = end_time - timedelta(minutes=5)

        overview = self.handler.get_overview(
            ticker='ETHUSDT',
            start=start_time,
            end=end_time
        )
        builtins.print('\n', overview)
