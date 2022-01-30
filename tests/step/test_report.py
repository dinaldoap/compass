from compass.step import ChangeHistoryReport

from datetime import datetime
import pandas as pd
from pandas.testing import assert_frame_equal


def test_change_history():
    input = pd.DataFrame(
        {
            "Date": [datetime(2022, 1, i) for i in range(1, 5)]
            + [datetime(2022, 2, i) for i in range(1, 3)],
            "Ticker": [
                "BITO39",
                "BITO39",
                "BITO39",
                "BITO39",
                "BIEF39",
                "BIEF39",
            ],
            "Change": [1, 1, -1, 1, 9, -9],
            "Price": [50.0, 150.0, 200.0, 200.0, 90.0, 90.0],
        }
    )
    expected = (
        input.assign(Expense=[0.5, 1.5, 2.0, 2.0, 0.9, 0.9])
        .assign(Value=[50.5, 151.5, 198.0, 202.0, 90.9, 89.1])
        .assign(CumSumChange=[1, 2, 1, 2, 9, 0])
        .assign(CumAvgExpense=[0.5, 1.0, 1.0, 1.5, 0.9, 0.9])
        .assign(CumSumExpense=[0.5, 2.0, 1.0, 3.0, 8.1, 0.0])
        .assign(CumAvgValue=[50.5, 101.0, 101.0, 151.5, 90.9, 90.9])
        .assign(CumSumValue=[50.5, 202.0, 101.0, 303.0, 818.1, 0.0])
        .assign(CapitalGain=[0.0, 0.0, 97.0, 0.0, 0.0, 0.0])
        .assign(Tax=[0.0, 0.0, 14.55, 0.0, 0.0, 0.0])
    )
    output = ChangeHistoryReport(expense_ratio=0.01, tax_rate=0.15).run(input)
    assert_frame_equal(expected, output)
