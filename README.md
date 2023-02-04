# C3tl

Depends on: [medici](https://github.com/e183b796621afbf902067460/medici), [c3f1nance](https://github.com/e183b796621afbf902067460/c3f1nance) and [trad3r](https://github.com/e183b796621afbf902067460/trad3r).

---
C3tl is an ETL-framework that helps to get the needed data from cryptocurrencies exchanges. The scalability of the framework is based on it's architecture that provides a simple way to scale up amount of a new handlers and add it to right factories. Each factory is an independent analytical unit and must located at abstract factory. Bridge helps to orchestrate of whole amount of factories and handlers.

# Installation
```
pip install git+https://github.com/e183b796621afbf902067460/c3tl.git#egg=c3tl
```

# Usage
For example, to get [`BinanceSpotWholeMarketTradesHandler`](https://github.com/e183b796621afbf902067460/c3tl/blob/master/c3tl/handlers/whole_market_trades_history/binance/handlers.py#L10) need to call [`C3BridgeConfigurator`](https://github.com/e183b796621afbf902067460/c3tl/blob/master/c3tl/bridge/configurator.py#L5) and pass to it constructor next arguments and then call `produce_handler()` method:

```python
from c3tl.abstract.fabric import c3Abstract
from c3tl.bridge.configurator import C3BridgeConfigurator


class_ = C3BridgeConfigurator(
    abstract=c3Abstract,
    fabric_name='whole_market_trades_history',
    handler_name='binance_spot'
).produce_handler()

handler = class_()
```

Current handler is `BinanceSpotWholeMarketTradesHandler`. After this we can call `get_overview()` method and pass ticker, start and end time in arguments to get the whole market trades from Binance SPOT section.
