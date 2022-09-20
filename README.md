# DeFi Overviews Fabric

Depends on: [defi-head-core](https://github.com/e183b796621afbf902067460/defi-head-core), [defi-providers-fabric](https://github.com/e183b796621afbf902067460/defi-providers-fabric), [defi-contracts-evm](https://github.com/e183b796621afbf902067460/defi-contracts-evm) and for tests will be needed [hybrid-traders-composite](https://github.com/e183b796621afbf902067460/hybrid-traders-composite)

---
Based on input arguments an `Abstract Fabric` return `Concrete Fabric` object such as: *Liquidity Pool Overview Fabric*, *Staking Pool Overview Fabric* or  *Lending Pool Overview Fabric*.
`Concrete Fabric` (Liquidity, Staking or Lending) can produce needed `IInstrumentOverview Object` for different purposes.

For example, to get `CurveLiquidityPoolOverview` need to call `BridgeConfigurator` and pass to it constructor next arguments and then call `produceProduct()` method:
```
from head.bridge.configurator import BridgeConfigurator
from overviews.abstracts.fabric import overviewAbstractFabric   


concreteFabricKey = 'liquidity-pool-overview'
concreteProductKey = 'curve'

overview = BridgeConfigurator(
            abstractFabric=overviewAbstractFabric,
            fabricKey=concreteFabricKey,
            productKey=concreteProductKey) \
            .produceProduct()
```

Current overview object is `CurveLiquidityPoolOverview`. After it's production need to set certain __properties__ to call `getOverview()` correctly. Let's see how it works in synergy:
```
from head.bridge.configurator import BridgeConfigurator

from providers.abstracts.fabric import providerAbstractFabric
from overviews.abstracts.fabric import overviewAbstractFabric
from traders.head.trader import headTrader


_address = '0xbEbc44782C7dB0a1A60Cb6fe97d0b483032FF1C7'


_provider = BridgeConfigurator(
            abstractFabric=providerAbstractFabric,
            fabricKey='http',
            productKey='eth') \
            .produceProduct()
            
overview = BridgeConfigurator(
            abstractFabric=overviewAbstractFabric,
            fabricKey='liquidity-pool-overview',
            productKey='curve') \
            .produceProduct()() \
            .setAddress(address=_address) \
            .setProvider(provider=_provider) \
            .setTrader(trader=headTrader) \
            .create()
```
After call `overview.getOverview()` it'll return a __Future__ object because it's a [@threadmethod](https://github.com/e183b796621afbf902067460/defi-head-core/blob/master/head/decorators/threadmethod.py), so if returned value is needed just call `overview.getOverview().result()`, but only for tests.
