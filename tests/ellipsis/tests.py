from providers.abstracts.fabric import providerAbstractFabric
from overviews.abstracts.fabric import overviewAbstractFabric
from traders.head.trader import headTrader
from head.bridge.configurator import BridgeConfigurator


provider = BridgeConfigurator(
    abstractFabric=providerAbstractFabric,
    fabricKey='http',
    productKey='bsc')\
    .produceProduct()

overviewContract = BridgeConfigurator(
    abstractFabric=overviewAbstractFabric,
    fabricKey='liquidity-pool-overview',
    productKey='ellipsis')\
    .produceProduct()()\
    .setAddress(address='0x160CAed03795365F3A589f10C379FfA7d75d4E76')\
    .setProvider(provider=provider)\
    .setTrader(trader=headTrader)\
    .create()


future = overviewContract.getOverview()
overview = future.result()

for aOverview in overview:
    assert isinstance(aOverview['symbol'], str)
    assert isinstance(aOverview['reserve'], (int, float))
    assert isinstance(aOverview['price'], (int, float))
