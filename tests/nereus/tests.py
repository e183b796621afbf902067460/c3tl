import unittest
from concurrent.futures import Future

import builtins

from overviews.protocols.nereus.overview import NereusLendingPoolOverview
from overviews.abstracts.fabric import overviewAbstractFabric

from providers.abstracts.fabric import providerAbstractFabric
from traders.head.trader import headTrader
from head.bridge.configurator import BridgeConfigurator


class TestNereusLendingPoolOverview(unittest.TestCase):

    _address = '0xB9257597EDdfA0eCaff04FF216939FBc31AAC026'

    _provider = BridgeConfigurator(
        abstractFabric=providerAbstractFabric,
        fabricKey='http',
        productKey='avax') \
        .produceProduct()

    _instance = BridgeConfigurator(
        abstractFabric=overviewAbstractFabric,
        fabricKey='lending-pool-overview',
        productKey='nereus') \
        .produceProduct()() \
        .setAddress(address=_address) \
        .setProvider(provider=_provider) \
        .setTrader(trader=headTrader) \
        .create()

    def testInstance(self):
        self.assertIsInstance(self._instance, NereusLendingPoolOverview)

    def testProvider(self):
        self.assertEqual(self._instance.provider, self._provider)

    def testAddress(self):
        self.assertEqual(self._instance.address, self._address)

    def testHead(self):
        self.assertEqual(self._instance.trader, headTrader)

    def test_getOverview(self):
        reserves = self._instance.getReservesList()

        futures = list()
        for reserve in reserves:
            future = self._instance.getOverview(asset=reserve)
            futures.append(future)
            self.assertIsInstance(future, Future)

        for future in futures:
            overview = future.result()
            self.assertIsInstance(overview, list)

            if overview:
                for aOverview in overview:
                    self.assertIsInstance(aOverview, dict)

                    self.assertIsInstance(aOverview['symbol'], str)
                    self.assertIsInstance(aOverview['reserve'], (int, float))
                    self.assertIsInstance(aOverview['borrow'], (int, float))
                    self.assertIsInstance(aOverview['price'], (int, float))
                builtins.print('\n', overview)
