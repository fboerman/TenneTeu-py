# TenneTeu-py
Python client for the official TenneT.eu api. Register for an API key go to the [API Develop Portal](https://developer.tennet.eu/).

If you want to mass download TenneT data, then don't do it through the API, you **will** hit rate limiters. Instead use the download page [here](https://www.tennet.eu/nl-en/grids-and-markets/transparency-data-netherlands/download-page-transparency) on the TenneT site.

DISCLAIMER: this is an _unofficial package_, do not contact TenneT about issues with the package, instead open an issue on this repo.

## Installation
`python3 -m pip install tenneteu-py`

## Usage
```python
from tenneteu import TenneTeuClient
from secret import apikey
import pandas as pd

client = TenneTeuClient(api_key=apikey)
d_from = pd.Timestamp('2024-01-01', tz='europe/amsterdam')
d_to = pd.Timestamp('2024-01-01 23:59', tz='europe/amsterdam')
# all possible queries listed below, name should be self explanatory
# from, to queries:
df = client.query_balance_delta(d_from=d_from, d_to=d_to)
df = client.query_settlement_prices(d_from=d_from, d_to=d_to)
df = client.query_merit_order_list(d_from=d_from, d_to=d_to)

#returns last 30 minutes like in tennet-py with the old api
df = client.query_current_imbalance() 
```