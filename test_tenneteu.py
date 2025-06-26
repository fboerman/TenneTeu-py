from dotenv import load_dotenv
from tenneteu import TenneTeuClient
import pytest
import pandas as pd

load_dotenv()


@pytest.fixture
def client():
    return TenneTeuClient()


@pytest.fixture
def d_from():
    return pd.Timestamp('2025-01-01 00:00', tz='europe/amsterdam')


@pytest.fixture
def d_to():
    return pd.Timestamp('2025-01-02 00:00', tz='europe/amsterdam')


def test_balance_delta(client, d_from, d_to):
    df = client.query_balance_delta(d_from=d_from, d_to=d_to)
    assert len(df) == 24*60
    assert list(df.columns) == ['Isp', 'Power In Activated Afrr', 'Power Out Activated Afrr', 'Power In Igcc',
                                'Power Out Igcc', 'Power In Mfrrda', 'Power Out Mfrrda',
                                'Highest Upward Regulation Price', 'Lowest Downward Regulation Price', 'Mid Price',
                                'Picasso Contribution Power In', 'Picasso Contribution Power Out']


def test_current_imbalance(client, d_from, d_to):
    df = client.query_current_imbalance()
    assert 27 <= len(df) <= 28
    assert list(df.columns) == ['Isp', 'Power In Activated Afrr', 'Power Out Activated Afrr', 'Power In Igcc',
                                'Power Out Igcc', 'Power In Mfrrda', 'Power Out Mfrrda',
                                'Highest Upward Regulation Price', 'Lowest Downward Regulation Price', 'Mid Price',
                                'Picasso Contribution Power In', 'Picasso Contribution Power Out']


def test_settlement_prices(client, d_from, d_to):
    df = client.query_settlement_prices(d_from=d_from, d_to=d_to)
    assert len(df) == 24*4
    assert list(df.columns) == ['Isp', 'Currency Unit Name', 'Price Measurement Unit Name', 'Incident Reserve Up',
                                'Incident Reserve Down', 'Price Dispatch Up', 'Price Dispatch Down', 'Price Shortage',
                                'Price Surplus', 'Regulation State', 'Regulating Condition']


def test_merit_order_list(client, d_from, d_to):
    df = client.query_merit_order_list(d_from=d_from, d_to=d_to)
    assert len(df) == 18085
    assert list(df.columns) == ['Isp', 'Quantity Measurement Unit Name', 'Price Measurement Unit Name',
                                'Currency Unit Name', 'Capacity Threshold', 'Price Down', 'Price Up']


def test_settled_imbalance_volumes(client, d_from, d_to):
    df = client.query_settled_imbalance_volumes(d_from=d_from, d_to=d_to)
    assert len(df) == 96
    assert list(df.columns) == ['Isp', 'Quantity Measurement Unit', 'Surplus', 'Shortage', 'Absolute', 'Imbalance']


def test_frequency_reserve_activations(client, d_from, d_to):
    df = client.query_frequency_reserve_activations(d_from, d_to)
    assert(len(df)) == 96
    assert list(df.columns) == ['Isp', 'Quantity Measurement Unit Name', 'Afrr Down', 'Afrr Up', 'Incident Reserve Down',
                                'Incident Reserve Up', 'Absolute Total Volume', 'Total Volume']
