import requests
import pandas as pd
from io import StringIO

__title__ = "tenneteu-py"
__version__ = "0.1.1"
__author__ = "Frank Boerman"
__license__ = "MIT"


class TenneTeuClient:
    BASEURL = "https://api.tennet.eu/publications/v1/"

    def __init__(self, api_key: str):
        self.s = requests.Session()
        self.s.headers.update({
            'user-agent': f'tenneteu-py {__version__} (github.com/fboerman/TenneTeu-py)',
            'Accept': 'text/csv',
            'apikey': api_key
        })

    def _base_query(self, url: str, d_from: pd.Timestamp, d_to: pd.Timestamp) -> str:
        r = self.s.get(self.BASEURL + url, params={
            'date_from': d_from.strftime('%d-%m-%Y %H:%M:%S'),
            'date_to': d_to.strftime('%d-%m-%Y %H:%M:%S')
        })
        r.raise_for_status()
        return r.text

    def _base_parse(self, csv_text) -> pd.DataFrame:
        stream = StringIO(csv_text)
        stream.seek(0)
        df = pd.read_csv(stream, sep=',')
        df['timestamp'] = pd.to_datetime(df['Timeinterval Start Loc'].str.split('T').str[0]).dt.tz_localize('europe/amsterdam') \
                          + (df['Isp']-1) * pd.Timedelta(minutes=15)
        return df.drop(columns=[
            'Timeinterval Start Loc',
            'Timeinterval End Loc'
        ]).set_index('timestamp')

    def query_balance_delta(self, d_from: pd.Timestamp, d_to: pd.Timestamp) -> pd.DataFrame:
        return self._base_parse(
            self._base_query(
                url='balance-delta',
                d_from=d_from,
                d_to=d_to
            )
        )

    def query_settlement_prices(self, d_from: pd.Timestamp, d_to: pd.Timestamp) -> pd.DataFrame:
        return self._base_parse(
            self._base_query(
                url='settlement-prices',
                d_from=d_from,
                d_to=d_to
            )
        )

    def query_merit_order_list(self, d_from: pd.Timestamp, d_to: pd.Timestamp) -> pd.DataFrame:
        return self._base_parse(
            self._base_query(
                url='merit-order-list',
                d_from=d_from,
                d_to=d_to
            )
        )

    def query_current_imbalance(self):
        d_to = pd.Timestamp.now(tz='europe/amsterdam')
        d_from = d_to - pd.Timedelta(minutes=32)
        return self.query_balance_delta(d_from, d_to)
