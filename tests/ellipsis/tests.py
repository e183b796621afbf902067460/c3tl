import unittest
from concurrent.futures import Future

import builtins

from overviews.protocols.ellipsis.overview import EllipsisDEXPoolOverview, EllipsisFarmingPoolAllocationOverview
from overviews.abstracts.fabric import overviewAbstractFabric

from providers.abstracts.fabric import providerAbstractFabric
from traders.head.trader import headTrader
from head.bridge.configurator import BridgeConfigurator


class TestEllipsisDEXPoolOverview(unittest.TestCase):

    _address = '0x160CAed03795365F3A589f10C379FfA7d75d4E76'

    _provider = BridgeConfigurator(
        abstractFabric=providerAbstractFabric,
        fabricKey='http',
        productKey='bsc') \
        .produceProduct()

    _instance = BridgeConfigurator(
        abstractFabric=overviewAbstractFabric,
        fabricKey='dex-pool-overview',
        productKey='ellipsis') \
        .produceProduct()() \
        .setAddress(address=_address) \
        .setProvider(provider=_provider) \
        .setTrader(trader=headTrader) \
        .create()

    def testInstance(self):
        self.assertIsInstance(self._instance, EllipsisDEXPoolOverview)

    def testProvider(self):
        self.assertEqual(self._instance.provider, self._provider)

    def testAddress(self):
        self.assertEqual(self._instance.address, self._address)

    def testHead(self):
        self.assertEqual(self._instance.trader, headTrader)

    def test_getOverview(self):
        future = self._instance.getOverview()
        self.assertIsInstance(future, Future)

        overview = future.result()
        self.assertIsInstance(overview, list)

        for aOverview in overview:
            self.assertIsInstance(aOverview, dict)

            self.assertIsInstance(aOverview['symbol'], str)
            self.assertIsInstance(aOverview['reserve'], (int, float))
            self.assertIsInstance(aOverview['price'], (int, float))
        builtins.print('\n', overview)


class TestEllipsisFarmingPoolAllocationOverview(unittest.TestCase):

    _address = '0xB343F4cDE5e2049857898E800CD385247e21836D'
    _wallet = '0x3DdfA8eC3052539b6C9549F12cEA2C295cfF5296'

    _provider = BridgeConfigurator(
        abstractFabric=providerAbstractFabric,
        fabricKey='http',
        productKey='bsc') \
        .produceProduct()

    _instance = BridgeConfigurator(
        abstractFabric=overviewAbstractFabric,
        fabricKey='farming-pool-allocation-overview',
        productKey='ellipsis') \
        .produceProduct()() \
        .setAddress(address=_address) \
        .setProvider(provider=_provider) \
        .setTrader(trader=headTrader) \
        .create()

    def testInstance(self):
        self.assertIsInstance(self._instance, EllipsisFarmingPoolAllocationOverview)

    def testProvider(self):
        self.assertEqual(self._instance.provider, self._provider)

    def testAddress(self):
        self.assertEqual(self._instance.address, self._address)

    def testHead(self):
        self.assertEqual(self._instance.trader, headTrader)

    def test_getOverview(self):
        future = self._instance.getOverview(address=self._wallet)
        self.assertIsInstance(future, Future)

        overview = future.result()
        self.assertIsInstance(overview, list)

        for aOverview in overview:
            self.assertIsInstance(aOverview, dict)

            self.assertIsInstance(aOverview['symbol'], str)
            self.assertIsInstance(aOverview['amount'], (int, float))
            self.assertIsInstance(aOverview['price'], (int, float))
        builtins.print('\n', overview)
