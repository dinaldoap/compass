import pandas as pd
from pandas.testing import assert_frame_equal

from compass.source.file import StandardActual
from compass.step import Actual


def test_actual():
    input = pd.DataFrame(
        {
            "Ticker": ["BITO39", "BIEF39"],
            "Target": [0.2, 0.8],
        }
    )
    expected = pd.DataFrame(
        {"Ticker": ["BITO39", "BIEF39"], "Target": [0.2, 0.8], "Actual": [1, 2]}
    )
    output = Actual(source=StandardActual(path="tests/data/actual.xlsx")).run(input)
    assert_frame_equal(expected, output[["Ticker", "Target", "Actual"]])
