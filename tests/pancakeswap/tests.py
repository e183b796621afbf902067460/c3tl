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
    productKey='pancakeswap')\
    .produceProduct()()\
    .setAddress(address='0x58F876857a02D6762E0101bb5C46A8c1ED44Dc16')\
    .setProvider(provider=provider)\
    .setTrader(trader=headTrader)\
    .create()


future = overviewContract.getOverview()
overview = future.result()

for aOverview in overview:
    assert isinstance(aOverview['symbol'], str)
    assert isinstance(aOverview['reserve'], (int, float))
    assert isinstance(aOverview['price'], (int, float))
