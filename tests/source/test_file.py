from compass.source.file import Standard, CEI

import pandas as pd
from pandas.testing import assert_frame_equal

def test_Standard():
    output = Standard('tests/data/actual_standard.xlsx').read()
    expected = pd.DataFrame({
        'Ticker': ['BITO39', 'BIEF39'],
        'Actual': [1, 2]
    })
    assert_frame_equal(expected, output[['Ticker', 'Actual']])

def test_CEI():
    output = CEI('tests/data/actual_cei.xlsx').read()
    expected = pd.DataFrame({
        'Ticker': ['BITO39', 'BIEF39'],
        'Actual': [1, 2]
    })
    assert_frame_equal(expected, output[['Ticker', 'Actual']])