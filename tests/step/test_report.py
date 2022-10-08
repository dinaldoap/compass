from cmath import exp
from compass.step import HistoricReport

from datetime import datetime
import pandas as pd
import numpy as np
from pandas.testing import assert_frame_equal


def test_change_history_avg_total():
    input = pd.DataFrame(
        {
            "Date": [datetime(2022, 1, i) for i in range(28, 32)]
            + [datetime(2022, 2, i) for i in range(27, 29)],
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
    ).set_index("Date")
    added_dates = pd.DataFrame(
        {
            "Date": [datetime(2022, 1, 31)] + [datetime(2022, 2, 28)],
            "Ticker": [
                "BIEF39",
                "BITO39",
            ],
            "Change": [0] * 2,
            "Price": [0.0] * 2,
        }
    ).set_index("Date")
    expected = (
        pd.concat([input, added_dates])
        .sort_values("Ticker")
        .sort_index()
        .assign(Expense=[0.5, 1.5, 2.0, 0.0, 2.0, 0.9, 0.9, 0.0])
        .assign(Value=[50.5, 151.5, 198.0, 0.0, 202.0, 90.9, 89.1, 0.0])
        .assign(Actual=[1, 2, 1, 0, 2, 9, 0, 2])
        .assign(AvgPrice=[50.0, 100.0, 100.0, 0.0, 150.0, 90.0, 90.0, 150.0])
        .assign(TotalPrice=[50.0, 200.0, 100.0, 0.0, 300.0, 810.0, 0.0, 300.0])
        .assign(AvgExpense=[0.5, 1.0, 1.0, 0.0, 1.5, 0.9, 0.9, 1.5])
        .assign(TotalExpense=[0.5, 2.0, 1.0, 0.0, 3.0, 8.1, 0.0, 3.0])
        .assign(AvgValue=[50.5, 101.0, 101.0, 0.0, 151.5, 90.9, 90.9, 151.5])
        .assign(TotalValue=[50.5, 202.0, 101.0, 0.0, 303.0, 818.1, 0.0, 303.0])
    )
    output = HistoricReport(
        expense_ratio=0.01, tax_rate=0.15, current_date=datetime(2022, 2, 28)
    ).run(input)
    assert_frame_equal(expected, output[expected.columns])


def test_change_history_capital_gain():
    input = pd.DataFrame(
        {
            "Date": [datetime(2022, 1, i) for i in range(28, 32)]
            + [datetime(2022, 2, i) for i in range(27, 29)]
            + [datetime(2022, 3, i) for i in range(30, 31)],
            "Ticker": [
                "BITO39",
                "BITO39",
                "BITO39",
                "BIEF39",
                "BIEF39",
                "BIEF39",
                "BIEF39",
            ],
            "Change": [2, -1, -1, 3, -1, -1, -1],
            "Price": [100.0, 50.0, 50.0, 100.0, 250.0, 200.0, 200],
        }
    ).set_index("Date")
    added_dates = pd.DataFrame(
        {
            "Date": [datetime(2022, 1, 31)]
            + [datetime(2022, 2, 28)]
            + [datetime(2022, 3, 31)] * 2,
            "Ticker": [
                "BITO39",
                "BITO39",
                "BIEF39",
                "BITO39",
            ],
            "Change": [0] * 4,
            "Price": [0.0] * 4,
        }
    ).set_index("Date")
    expected = (
        pd.concat([input, added_dates])
        .sort_index()
        .assign(
            Value=[100.0, 50.0, 50.0, 100.0, 0.0, 250.0, 200.0, 0.0, 200.0, 0.0, 0.0]
        )
        .assign(
            AvgValue=[
                100.0,
                100.0,
                100.0,
                100.0,
                0.0,
                100.0,
                100.0,
                0.0,
                100.0,
                0.0,
                0.0,
            ]
        )
        .assign(
            CapitalGain=[
                0.0,
                -50.0,
                -50.0,
                0.0,
                0.0,
                150.0,
                100.0,
                0.0,
                100.0,
                0.0,
                0.0,
            ]
        )
        .assign(
            TotalCapitalGain=[
                0.0,
                -50.0,
                -100.0,
                -100.0,
                -100.0,
                50.0,
                150.0,
                150.0,
                100.0,
                100.0,
                100.0,
            ]
        )
        .assign(Tax=[0.0, 0.0, 0.0, 0.0, 0.0, 7.5, 22.5, 22.5, 15.0, 15.0, 15.0])
    )
    output = HistoricReport(
        expense_ratio=0.0, tax_rate=0.15, current_date=datetime(2022, 3, 31)
    ).run(input)
    print(expected)
    print(output)
    assert_frame_equal(expected, output[expected.columns])
