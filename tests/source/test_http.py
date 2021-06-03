from compass.source.http import *

import pandas as pd
from pandas.testing import assert_frame_equal
from pathlib import Path

def test_YahooPrice():
    output = YahooPrice(Path('tests/data')).read(tickers=['BITO39'])
    expected = pd.DataFrame({
        'Ticker': ['BITO39'],
        'Price': [53.40]
    })
    assert_frame_equal(expected, output[['Ticker', 'Price']])