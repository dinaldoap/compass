from compass.step import Actual

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
        'Actual': [0, 0]
    })
    output = Actual().run(input)
    assert_frame_equal(expected, output[['Ticker', 'Target', 'Actual']])