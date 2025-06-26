import requests
import pandas as pd
from io import StringIO
import os

__title__ = "tenneteu-py"
__version__ = "0.1.3"
__author__ = "Frank Boerman"
__license__ = "MIT"


class TenneTeuClient:
    BASEURL = "https://api.tennet.eu/publications/v1/"

    def __init__(self, api_key: str = None, acce: bool = False):
        if api_key is None:
            api_key = os.environ.get('TENNET_API_KEY')
            if api_key is None:
                raise Exception('Please provide an api key either through function argument or env')
        if acce:
            self.BASEURL = self.BASEURL.replace('api.', 'api.acc.')
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

    def _base_parse(self, csv_text, minutes) -> pd.DataFrame:
        stream = StringIO(csv_text)
        stream.seek(0)
        df = pd.read_csv(stream, sep=',')
        df['timestamp'] = pd.to_datetime(df['Timeinterval Start Loc'].str.split('T').str[0]).dt.tz_localize('europe/amsterdam') \
                          + (df['Isp']-1) * pd.Timedelta(minutes=minutes)
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
            ),
            minutes=1
        )

    def query_settlement_prices(self, d_from: pd.Timestamp, d_to: pd.Timestamp) -> pd.DataFrame:
        return self._base_parse(
            self._base_query(
                url='settlement-prices',
                d_from=d_from,
                d_to=d_to
            ),
            minutes=15
        )

    def query_merit_order_list(self, d_from: pd.Timestamp, d_to: pd.Timestamp) -> pd.DataFrame:
        return self._base_parse(
            self._base_query(
                url='merit-order-list',
                d_from=d_from,
                d_to=d_to
            ),
            minutes=15
        )

    def query_settled_imbalance_volumes(self, d_from: pd.Timestamp, d_to: pd.Timestamp) -> pd.DataFrame:
        return self._base_parse(
            self._base_query(
                url='settled-imbalance-volumes',
                d_from=d_from,
                d_to=d_to
            ),
            minutes=15
        )

    def query_frequency_reserve_activations(self, d_from: pd.Timestamp, d_to: pd.Timestamp) -> pd.DataFrame:
        return self._base_parse(
            self._base_query(
                url='frequency-restoration-reserve-activations',
                d_from=d_from,
                d_to=d_to
            ),
            minutes=15
        )

    def query_current_imbalance(self):
        d_to = pd.Timestamp.now(tz='europe/amsterdam')
        d_from = d_to - pd.Timedelta(minutes=32)
        return self.query_balance_delta(d_from, d_to)
