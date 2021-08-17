from compass.step import Actual, ActualAddedChange
from compass.source.file import StandardActual, StandardOutput

import pandas as pd
from pandas.testing import assert_frame_equal


def test_actual():
    input = pd.DataFrame({
        'Ticker': ['BITO39', 'BIEF39'],
        'Target': [.2, .8],
    })
    expected = pd.DataFrame({
        'Ticker': ['BITO39', 'BIEF39'],
        'Target': [.2, .8],
        'Actual': [1, 2]
    })
    output = Actual(source=StandardActual(
        path='tests/data/actual.xlsx')).run(input)
    assert_frame_equal(expected, output[['Ticker', 'Target', 'Actual']])


def test_actual_added_change():
    input = pd.DataFrame({
        'Ticker': ['BITO39', 'BIEF39'],
        'Actual': [1, 2],
    })
    expected = pd.DataFrame({
        'Ticker': ['BITO39', 'BIEF39'],
        'Actual': [2, 4]
    })
    output = ActualAddedChange(source=StandardOutput(
        'tests/data/output.xlsx')).run(input)
    assert_frame_equal(expected, output[['Ticker', 'Actual']])
