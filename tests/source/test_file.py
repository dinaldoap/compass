from compass.source.file import *

import pandas as pd
from pandas.testing import assert_frame_equal

def test_StandardTarget():
    output = StandardTarget('tests/data/target.xlsx').read()
    expected = pd.DataFrame({
        'Name': ['iShares Core S&P Total US Stock Market ETF', 'iShares Core MSCI EAFE ETF'],
        'Ticker': ['BITO39', 'BIEF39'],
        'Target': [.2, .8]
    })
    assert_frame_equal(expected, output[['Name', 'Ticker', 'Target']])

def test_StandardActual():
    output = StandardActual('tests/data/actual_standard.xlsx').read()
    expected = pd.DataFrame({
        'Ticker': ['BITO39', 'BIEF39'],
        'Actual': [1, 2]
    })
    assert_frame_equal(expected, output[['Ticker', 'Actual']])

def test_CEIActual():
    output = CeiActual('tests/data/actual.xlsx').read()
    expected = pd.DataFrame({
        'Ticker': ['BITO39', 'BIEF39'],
        'Actual': [1, 2]
    })
    assert_frame_equal(expected, output[['Ticker', 'Actual']])

def test_StandardPrice():
    output = StandardPrice('tests/data/price.xlsx').read()
    expected = pd.DataFrame({
        'Ticker': ['BITO39', 'BIEF39', 'BIEM39'],
        'Price': [1, 2, 3]
    })
    assert_frame_equal(expected, output[['Ticker', 'Price']])