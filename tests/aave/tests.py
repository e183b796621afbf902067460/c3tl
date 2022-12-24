import unittest
from concurrent.futures import Future

import builtins

from overviews.protocols.aave.overview import (
    AaveV2LendingPoolOverview, AaveV2LendingPoolAllocationOverview, AaveV2LendingPoolBorrowOverview,
    AaveV2LendingPoolIncentiveOverview
)
from overviews.abstracts.fabric import overviewAbstractFabric

from providers.abstracts.fabric import providerAbstractFabric
from traders.head.trader import headTrader
from head.bridge.configurator import BridgeConfigurator


class TestAaveLendingPoolOverview(unittest.TestCase):

    _address = '0x7d2768dE32b0b80b7a3454c06BdAc94A69DDc7A9'

    _provider = BridgeConfigurator(
        abstractFabric=providerAbstractFabric,
        fabricKey='http',
        productKey='eth') \
        .produceProduct()

    _instance = BridgeConfigurator(
        abstractFabric=overviewAbstractFabric,
        fabricKey='lending-pool-overview',
        productKey='aave') \
        .produceProduct()() \
        .setAddress(address=_address) \
        .setProvider(provider=_provider) \
        .setTrader(trader=headTrader) \
        .create()

    def testInstance(self):
        self.assertIsInstance(self._instance, AaveV2LendingPoolOverview)

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


class TestAaveV2LendingPoolAllocationOverview(unittest.TestCase):

    _address = '0x7d2768dE32b0b80b7a3454c06BdAc94A69DDc7A9'
    _wallet = '0x7344E478574aCBe6DaC9dE1077430139E17EEc3D'

    _provider = BridgeConfigurator(
        abstractFabric=providerAbstractFabric,
        fabricKey='http',
        productKey='eth') \
        .produceProduct()

    _instance = BridgeConfigurator(
        abstractFabric=overviewAbstractFabric,
        fabricKey='lending-pool-allocation-overview',
        productKey='aave') \
        .produceProduct()() \
        .setAddress(address=_address) \
        .setProvider(provider=_provider) \
        .setTrader(trader=headTrader) \
        .create()

    def testInstance(self):
        self.assertIsInstance(self._instance, AaveV2LendingPoolAllocationOverview)

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


class TestAaveV2LendingPoolBorrowOverview(unittest.TestCase):

    _address = '0x7d2768dE32b0b80b7a3454c06BdAc94A69DDc7A9'
    _wallet = '0x7344E478574aCBe6DaC9dE1077430139E17EEc3D'

    _provider = BridgeConfigurator(
        abstractFabric=providerAbstractFabric,
        fabricKey='http',
        productKey='eth') \
        .produceProduct()

    _instance = BridgeConfigurator(
        abstractFabric=overviewAbstractFabric,
        fabricKey='lending-pool-borrow-overview',
        productKey='aave') \
        .produceProduct()() \
        .setAddress(address=_address) \
        .setProvider(provider=_provider) \
        .setTrader(trader=headTrader) \
        .create()

    def testInstance(self):
        self.assertIsInstance(self._instance, AaveV2LendingPoolBorrowOverview)

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


class TestAaveV2LendingPoolIncentivesOverview(unittest.TestCase):

    _address = '0x7d2768dE32b0b80b7a3454c06BdAc94A69DDc7A9'
    _wallet = '0x13873fa4B7771F3492825B00D1c37301fF41C348'

    _provider = BridgeConfigurator(
        abstractFabric=providerAbstractFabric,
        fabricKey='http',
        productKey='eth') \
        .produceProduct()

    _instance = BridgeConfigurator(
        abstractFabric=overviewAbstractFabric,
        fabricKey='lending-pool-incentive-overview',
        productKey='aave') \
        .produceProduct()() \
        .setAddress(address=_address) \
        .setProvider(provider=_provider) \
        .setTrader(trader=headTrader) \
        .create()

    def testInstance(self):
        self.assertIsInstance(self._instance, AaveV2LendingPoolIncentiveOverview)

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
