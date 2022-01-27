from compass.step import ChangeHistoryReport

import pandas as pd
from pandas.testing import assert_frame_equal


def test_change_history():
    input = pd.DataFrame(
        {
            "Date": [f"{i:02}/01/2022" for i in range(1, 6)],
            "Ticker": [
                "BITO39",
                "BITO39",
                "BITO39",
                "BITO39",
                "BIEF39",
            ],
            "Change": [1, 1, -1, 1, 9],
            "Price": [0.5, 1.5, 2.0, 2.0, 9.0],
        }
    )
    expected = input.assign(AvgPrice=[0.5, 1, 1, 1.5, 9.0]).assign(
        CapitalGain=[0.0, 0.0, 1.0, 0.0, 0.0]
    )
    output = ChangeHistoryReport().run(input)
    assert_frame_equal(expected, output)
