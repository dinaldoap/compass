from compass.source.file import *

import pandas as pd
from pandas.testing import assert_frame_equal

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