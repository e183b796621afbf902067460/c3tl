import unittest
from concurrent.futures import Future

import builtins

from overviews.protocols.nereus.overview import (
    NereusLendingPoolOverview, NereusLendingPoolAllocationOverview, NereusLendingPoolBorrowOverview,
    NereusLendingPoolIncentiveOverview
)
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
        future = self._instance.getOverview()
        self.assertIsInstance(future, Future)

        overview = future.result()
        self.assertIsInstance(overview, list)

        for aOverview in overview:
            self.assertIsInstance(aOverview, dict)

            self.assertIsInstance(aOverview['pit_token_symbol'], str)
            self.assertIsInstance(aOverview['pit_token_reserve_size'], (int, float))
            self.assertIsInstance(aOverview['pit_token_borrow_size'], (int, float))
            self.assertIsInstance(aOverview['pit_token_price'], (int, float))
            self.assertIsInstance(aOverview['pit_token_deposit_apy'], (int, float))
            self.assertIsInstance(aOverview['pit_token_borrow_apy'], (int, float))
        builtins.print('\n', overview)


class TestNereusLendingPoolAllocationOverview(unittest.TestCase):

    _address = '0xB9257597EDdfA0eCaff04FF216939FBc31AAC026'
    _wallet = '0xE3f277382419535245a345e923898c2d43f7CBE5'

    _provider = BridgeConfigurator(
        abstractFabric=providerAbstractFabric,
        fabricKey='http',
        productKey='avax') \
        .produceProduct()

    _instance = BridgeConfigurator(
        abstractFabric=overviewAbstractFabric,
        fabricKey='lending-pool-allocation-overview',
        productKey='nereus') \
        .produceProduct()() \
        .setAddress(address=_address) \
        .setProvider(provider=_provider) \
        .setTrader(trader=headTrader) \
        .create()

    def testInstance(self):
        self.assertIsInstance(self._instance, NereusLendingPoolAllocationOverview)

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

            self.assertIsInstance(aOverview['pit_token_symbol'], str)
            self.assertIsInstance(aOverview['pit_token_amount'], (int, float))
            self.assertIsInstance(aOverview['pit_token_price'], (int, float))
        builtins.print('\n', overview)


class TestNereusLendingPoolBorrowOverview(unittest.TestCase):

    _address = '0xB9257597EDdfA0eCaff04FF216939FBc31AAC026'
    _wallet = '0xE3f277382419535245a345e923898c2d43f7CBE5'

    _provider = BridgeConfigurator(
        abstractFabric=providerAbstractFabric,
        fabricKey='http',
        productKey='avax') \
        .produceProduct()

    _instance = BridgeConfigurator(
        abstractFabric=overviewAbstractFabric,
        fabricKey='lending-pool-borrow-overview',
        productKey='nereus') \
        .produceProduct()() \
        .setAddress(address=_address) \
        .setProvider(provider=_provider) \
        .setTrader(trader=headTrader) \
        .create()

    def testInstance(self):
        self.assertIsInstance(self._instance, NereusLendingPoolBorrowOverview)

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

            self.assertIsInstance(aOverview['pit_token_symbol'], str)
            self.assertIsInstance(aOverview['pit_token_amount'], (int, float))
            self.assertIsInstance(aOverview['pit_token_price'], (int, float))
            self.assertIsInstance(aOverview['pit_health_factor'], (int, float))
        builtins.print('\n', overview)


class TestNereusLendingPoolIncentiveOverview(unittest.TestCase):

    _address = '0xB9257597EDdfA0eCaff04FF216939FBc31AAC026'
    _wallet = '0xE3f277382419535245a345e923898c2d43f7CBE5'

    _provider = BridgeConfigurator(
        abstractFabric=providerAbstractFabric,
        fabricKey='http',
        productKey='avax') \
        .produceProduct()

    _instance = BridgeConfigurator(
        abstractFabric=overviewAbstractFabric,
        fabricKey='lending-pool-incentive-overview',
        productKey='nereus') \
        .produceProduct()() \
        .setAddress(address=_address) \
        .setProvider(provider=_provider) \
        .setTrader(trader=headTrader) \
        .create()

    def testInstance(self):
        self.assertIsInstance(self._instance, NereusLendingPoolIncentiveOverview)

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

            self.assertIsInstance(aOverview['pit_token_symbol'], str)
            self.assertIsInstance(aOverview['pit_token_amount'], (int, float))
            self.assertIsInstance(aOverview['pit_token_price'], (int, float))
        builtins.print('\n', overview)
