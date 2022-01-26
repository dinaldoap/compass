from compass.source import Source
from compass.step import Join

import pandas as pd
from pandas.testing import assert_frame_equal


class SourceMock(Source):
    def read(self):
        # BIEF39 is missing value
        return pd.DataFrame({"Ticker": ["BITO39"], "Actual": [1]})


def test_join():
    input = pd.DataFrame(
        {
            "Ticker": ["BITO39", "BIEF39"],
            "Target": [0.2, 0.8],
        }
    )
    expected = pd.DataFrame(
        {"Ticker": ["BITO39", "BIEF39"], "Target": [0.2, 0.8], "Actual": [1, 2]}
    )
    # Left join requires filling BIEF39's actual
    output = Join(source=SourceMock(), on="Ticker", fillna={"Actual": 2}).run(input)
    assert_frame_equal(expected, output)
