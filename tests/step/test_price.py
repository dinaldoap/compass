from compass.source.file import StandardPrice
from compass.step import Price
from compass.source.file import StandardPrice

import pandas as pd
from pandas.testing import assert_frame_equal


def test_price():
    input = pd.DataFrame(
        {
            "Ticker": ["BITO39", "BIEF39"],
        }
    )
    expected = pd.DataFrame({"Ticker": ["BITO39", "BIEF39"], "Price": [1, 2]})
    output = Price(source=StandardPrice("tests/data/price.xlsx")).run(input)
    assert_frame_equal(expected, output)
