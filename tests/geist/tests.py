import unittest
from concurrent.futures import Future

import builtins

from overviews.protocols.geist.overview import (
    GeistLendingPoolOverview, GeistLendingPoolAllocationOverview, GeistLendingPoolBorrowOverview
)
from overviews.abstracts.fabric import overviewAbstractFabric

from providers.abstracts.fabric import providerAbstractFabric
from traders.head.trader import headTrader
from head.bridge.configurator import BridgeConfigurator


class TestGeistLendingPoolOverview(unittest.TestCase):

    _address = '0x9FAD24f572045c7869117160A571B2e50b10d068'

    _provider = BridgeConfigurator(
        abstractFabric=providerAbstractFabric,
        fabricKey='http',
        productKey='ftm') \
        .produceProduct()

    _instance = BridgeConfigurator(
        abstractFabric=overviewAbstractFabric,
        fabricKey='lending-pool-overview',
        productKey='geist') \
        .produceProduct()() \
        .setAddress(address=_address) \
        .setProvider(provider=_provider) \
        .setTrader(trader=headTrader) \
        .create()

    def testInstance(self):
        self.assertIsInstance(self._instance, GeistLendingPoolOverview)

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
            self.assertIsInstance(aOverview['depositAPY'], (int, float))
            self.assertIsInstance(aOverview['borrowAPY'], (int, float))
        builtins.print('\n', overview)


class TestGeistLendingPoolAllocationOverview(unittest.TestCase):

    _address = '0x9FAD24f572045c7869117160A571B2e50b10d068'
    _wallet = '0xbbbb1e5810998581F7977E9F5fa98a3250Cb809f'

    _provider = BridgeConfigurator(
        abstractFabric=providerAbstractFabric,
        fabricKey='http',
        productKey='ftm') \
        .produceProduct()

    _instance = BridgeConfigurator(
        abstractFabric=overviewAbstractFabric,
        fabricKey='lending-pool-allocation-overview',
        productKey='geist') \
        .produceProduct()() \
        .setAddress(address=_address) \
        .setProvider(provider=_provider) \
        .setTrader(trader=headTrader) \
        .create()

    def testInstance(self):
        self.assertIsInstance(self._instance, GeistLendingPoolAllocationOverview)

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


class TestGeistLendingPoolBorrowOverview(unittest.TestCase):

    _address = '0x9FAD24f572045c7869117160A571B2e50b10d068'
    _wallet = '0xbbbb1e5810998581F7977E9F5fa98a3250Cb809f'

    _provider = BridgeConfigurator(
        abstractFabric=providerAbstractFabric,
        fabricKey='http',
        productKey='ftm') \
        .produceProduct()

    _instance = BridgeConfigurator(
        abstractFabric=overviewAbstractFabric,
        fabricKey='lending-pool-borrow-overview',
        productKey='geist') \
        .produceProduct()() \
        .setAddress(address=_address) \
        .setProvider(provider=_provider) \
        .setTrader(trader=headTrader) \
        .create()

    def testInstance(self):
        self.assertIsInstance(self._instance, GeistLendingPoolBorrowOverview)

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
            self.assertIsInstance(aOverview['healthFactor'], (int, float))
        builtins.print('\n', overview)
