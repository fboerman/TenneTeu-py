# TenneTeu-py
Python client for the official tennet.eu api. Currently the API is only open for accredited parties, please contact Customer Contact Center (tennetccc@tennet.eu) for access.

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