from pathlib import Path

import pandas as pd
from pandas.testing import assert_frame_equal

from compass.source import Source
from compass.source.http import *


class MockTargetSource(Source):
    def read(self) -> pd.DataFrame:
        return pd.DataFrame({"Ticker": ["BITO39"]})


def test_YahooPrice():
    output = YahooPrice(Path("tests/data"), target=MockTargetSource()).read()
    expected = pd.DataFrame({"Ticker": ["BITO39"], "Price": [53.40]})
    assert_frame_equal(expected, output[["Ticker", "Price"]])
