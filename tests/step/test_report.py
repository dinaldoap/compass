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
            "Price": [50.0, 150.0, 200.0, 200.0, 90.0],
        }
    )
    expected = (
        input.assign(AvgPrice=[50.0, 100.0, 100.0, 150.0, 90])
        .assign(Expense=[0.5, 1.5, 2.0, 2.0, 0.9])
        .assign(CapitalGain=[0.0, 0.0, 100.0, 0.0, 0.0])
        .assign(Taxes=[0.0, 0.0, 15.0, 0.0, 0.0])
    )
    output = ChangeHistoryReport(expense_ratio=0.01, tax_rate=0.15).run(input)
    assert_frame_equal(expected, output)
