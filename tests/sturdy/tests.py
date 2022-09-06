from providers.abstracts.fabric import providerAbstractFabric
from overviews.abstracts.fabric import overviewAbstractFabric
from traders.head.trader import headTrader
from head.bridge.configurator import BridgeConfigurator


provider = BridgeConfigurator(
    abstractFabric=providerAbstractFabric,
    fabricKey='http',
    productKey='eth')\
    .produceProduct()

overviewContract = BridgeConfigurator(
    abstractFabric=overviewAbstractFabric,
    fabricKey='lending-pool-overview',
    productKey='sturdy')\
    .produceProduct()()\
    .setAddress(address='0xA422CA380bd70EeF876292839222159E41AAEe17')\
    .setProvider(provider=provider)\
    .setTrader(trader=headTrader)\
    .create()


assets = overviewContract.getReservesList()


futures = list()
for asset in assets:
    future = overviewContract.getOverview(asset)
    futures.append(future)

for future in futures:
    overview = future.result()
    if overview:
        for aOverview in overview:
            assert isinstance(aOverview['reserve'], (int, float))
            assert isinstance(aOverview['borrow'], (int, float))
            assert isinstance(aOverview['price'], (int, float))
